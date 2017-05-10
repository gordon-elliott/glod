__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene
from graphene import Connection, ConnectionField, Node, PageInfo
from graphql_relay.connection.arrayconnection import offset_to_cursor

from a_tuin.metadata import Mapping, PartialDictFieldGroup
from a_tuin.api import with_session, get_input_fields


def node_connection_field(model_class, query_class, node_class, description):
    """ Make a ConnectionField for a model class

    :param query_class: query class for model
    :param node_class: ObjectType
    :param description: string describing the collection
    :return: ConnectionField
    """
    entity_name = model_class.__name__

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
        '{}NodeConnection'.format(entity_name),
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
    filter_to_internal = Mapping(untyped_filter_field_group, typed_filter_field_group)

    @with_session
    def resolver(self, args, context, info, session):
        query = query_class(session)

        filters = args.get('filters')
        if filters:
            typed = filter_to_internal.cast_from(filters, allow_partial=True)
            criteria = tuple(query.criteria_from_dict(typed))
            query.filter(*criteria)

        filtered_count = len(query)

        after = args.get('after')
        if after:
            offset = int(Node.from_global_id(after)[1])
            query.offset(offset)
            args.pop('after')

        first = args.get('first')
        if first:
            limit = int(first)
            query.limit(limit)

        instance_generator = query.collection()
        instances = list(instance_generator)
        context['count'] = len(instances)
        context['pageInfo'] = PageInfo(
            start_cursor=offset_to_cursor(query.start_index),
            end_cursor=offset_to_cursor(query.end_index),
            has_previous_page=query.start_index > 0,
            has_next_page=query.end_index < filtered_count - 1
        )
        return instances

    # equivalent to
    # class SomeFilterInput(graphene.InputObjectType):
    #   refNo = graphene.Argument(graphene.Int)
    #   ...
    filter_input = type(
        '{}FilterInput'.format(entity_name),
        (graphene.InputObjectType,),
        get_input_fields(model_class)
    )

    connection_field = ConnectionField(
        connection_class,
        resolver=resolver,
        description=description,
        filters=graphene.Argument(filter_input),
    )

    return connection_field
