__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene
from graphene import Connection, ConnectionField

from a_tuin.api import with_session


def node_connection_field(query_class, node_class, description):
    """ Make a ConnectionField for a model class

    :param query_class: query class for model
    :param node_class: ObjectType
    :param description: string describing the collection
    :return: ConnectionField
    """
    entity_name = query_class.__name__

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

    @with_session
    def resolver(self, args, context, info, session):
        query = query_class(session)
        accounts = list(query.collection())
        context['count'] = len(accounts)
        return accounts

    connection_field = ConnectionField(
        connection_class,
        resolver=resolver,
        description=description,
        # filter=graphene.Argument(leaf_class),
    )

    # TODO start here - design filter input atom and collection

    return connection_field
