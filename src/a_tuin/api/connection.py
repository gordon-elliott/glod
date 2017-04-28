__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene
from graphene import Connection, ConnectionField

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
        instances = list(query.collection())
        context['count'] = len(instances)
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
