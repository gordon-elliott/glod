__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from collections import OrderedDict
from graphene import Connection, ConnectionField, Node, PageInfo
from graphql_relay.connection.arrayconnection import (
    offset_to_cursor,
    connection_from_list_slice as connection_from_list_slice_unpatched
)
from graphql_relay.connection import arrayconnection

from a_tuin.metadata import Mapping, PartialDictFieldGroup, make_boolean, snake_to_camel_case
from a_tuin.metadata.reference import references_from
from a_tuin.api import with_session, get_filter_fields, OBJECT_REFERENCE_MAP


def connection_from_list_slice_patch(list_slice, args=None, connection_type=None,
                               edge_type=None, pageinfo_type=None,
                               slice_start=0, list_length=0, list_slice_length=None):

    # remove before and after because they prevent server-side paging
    for argument_name in ('before', 'after'):
        if argument_name in args:
            del args[argument_name]

    return connection_from_list_slice_unpatched(list_slice, args, connection_type,
                               edge_type, pageinfo_type,
                               slice_start, list_length, list_slice_length)


arrayconnection.connection_from_list_slice = connection_from_list_slice_patch


def _parse_order_by(order_by_string):
    for column_spec in order_by_string.split(','):
        if column_spec[0] == '-':
            column_spec = column_spec[1:]
            sort_ascending = False
        else:
            sort_ascending = True
        yield column_spec, sort_ascending


def _instance_id_from_global_id(global_id, _):
    _, id_ = graphene.Node.from_global_id(global_id)
    return id_


def _filter_casts(model_class, typed_filter_field_group):
    filter_casts = {}
    for reference in references_from(model_class):
        # map relations on to a column that the mapper can identify
        for field in typed_filter_field_group:
            if field.name == reference.source_field_internal_name:
                field.name = reference.relation_map.fk_fieldname
        # cast global id to instance id
        filter_casts[reference.source_field_public_name] = _instance_id_from_global_id
    return filter_casts


def node_connection_field(model_class, query_class, node_class, description):
    """ Make a ConnectionField for a model class

    :param query_class: query class for model
    :param node_class: ObjectType
    :param description: string describing the collection
    :return: ConnectionField
    """
    entity_name = node_class.__name__

    class NodeConnection(object):
        @with_session
        def resolve_total_count(self, args, context, info, session):
            return len(query_class(session))

        @with_session
        def resolve_filtered_count(self, args, context, info, session):
            return context['count']

        @with_session
        def resolve_page_info(self, args, context, info, session):
            return context['pageInfo']

    connection_class = type(
        '{}Connection'.format(entity_name),
        # inherit class methods from NodeConnection and other behaviour from
        # graphene.relay.Connection
        (NodeConnection, Connection),
        # equivalent to
        # total_count = graphene.Int()
        # filtered_count = graphene.Int()
        # class Meta:
        #     node = node_class
        {
            'total_count': graphene.Int(),
            'filtered_count': graphene.Int(),
            'Meta': type('Meta', (object,), {'node': node_class,})
        }
    )

    untyped_filter_field_group = model_class.properties.derive(field_group_class=PartialDictFieldGroup)
    typed_filter_field_group = model_class.internal.derive(field_group_class=PartialDictFieldGroup)
    filter_casts = _filter_casts(model_class, typed_filter_field_group)
    filter_to_internal = Mapping(untyped_filter_field_group, typed_filter_field_group, field_casts=filter_casts)

    camel_case_field_group = model_class.properties.derive(snake_to_camel_case, PartialDictFieldGroup)
    order_by_field_group = model_class.internal.derive(make_boolean, PartialDictFieldGroup)
    order_by_to_mapped = Mapping(camel_case_field_group, order_by_field_group)

    @with_session
    def resolver(self, args, context, info, session):
        query = query_class(session)

        filters = args.get('filters')
        if filters:
            typed = filter_to_internal.cast_from(filters)
            criteria = tuple(query.criteria_from_dict(typed))
            query.filter(*criteria)

        filtered_count = len(query)

        order_by = args.get('orderBy')
        if order_by:
            order_by_values = OrderedDict(_parse_order_by(order_by))
            mapped = order_by_to_mapped.cast_from(order_by_values)
            # TODO only add this sort by id if there is no other sort by a unique field
            # required in order have stable sorting and paging when sorting by a non-unique field
            mapped['_id'] = True
            criteria = tuple(query.sort_criteria_from_dict(mapped))
            query.order_by(*criteria)

        offset = 0
        after = args.get('after')
        if after:
            offset = int(Node.from_global_id(after)[1])
            query.offset(offset)
            offset += 1
            args.pop('after')

        first = args.get('first')
        if first:
            limit = int(first)
            query.limit(limit)

        instances = list(query.collection())

        context['count'] = filtered_count
        context['pageInfo'] = PageInfo(
            start_cursor=offset_to_cursor(query.start_index),
            end_cursor=offset_to_cursor(query.end_index),
            has_previous_page=False if query.start_index is None else query.start_index > 0,
            has_next_page=False if query.end_index is None else query.end_index < filtered_count - 1
        )
        return instances

    # equivalent to
    # class SomeFilterInput(graphene.InputObjectType):
    #   refNo = graphene.Argument(graphene.Int)
    #   ...
    filter_input = type(
        '{}FilterInput'.format(entity_name),
        (graphene.InputObjectType,),
        get_filter_fields(model_class)
    )

    connection_field = ConnectionField(
        connection_class,
        resolver=resolver,
        description=description,
        filters=graphene.Argument(filter_input),
        orderBy=graphene.Argument(graphene.String),
    )

    return connection_field
