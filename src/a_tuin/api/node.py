__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from graphene import Node, Interface


def node_class(entity_name, leaf_class, node_fields):

    # node_class is based on the Leaf class but may include collections
    # of related objects; results can also be paged, filtered and sorted
    node_class = type(
        # e.g. AccountNode
        '{}Node'.format(entity_name),
        # inherit from the leaf class
        (leaf_class,),
        # equivalent to
        # class Meta:
        #   interfaces = (Node, type('NodeFields', (Interface,), node_fields))
        {'Meta': type('Meta', (object,), {
            'interfaces': (
                Node,
                type('{}NodeFields'.format(entity_name), (Interface,), node_fields)
            ),
        })}
    )
    return node_class
