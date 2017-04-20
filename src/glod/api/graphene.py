__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from collections import OrderedDict

from graphene import Node, Connection, ConnectionField
from graphene.relay import ClientIDMutation
from glod.model.references import references_from
from glod.api.types import GRAPHENE_FIELD_TYPE_MAP, OBJECT_REFERENCE_MAP

# TODO consider moving to a_tuin

ID_FIELD_NAME = 'id'


def _map_field(field):
    """ Produce a Graphene field for a model metadata Field

    :param field a_tuin.metadata.Field:
    :return: graphene.Field
    """
    graphene_field_type = GRAPHENE_FIELD_TYPE_MAP.get(type(field))
    if graphene_field_type is None:
        if hasattr(field, 'enum_class'):
            graphene_field_type = graphene.Enum.from_enum(field.enum_class)
        else:
            return graphene.Field(OBJECT_REFERENCE_MAP[field.name])

    return graphene.Field.mounted(graphene_field_type())


def get_local_fields(model_class):
    """ Use model metadata to produce Graphene Fields

    :param model_class: class to inspect
    :return: OrderedDict of fieldname to Graphene Field
    """
    return OrderedDict(
        (field.name, _map_field(field))
        for field in model_class.constructor_parameters
    )


def with_session(fn):
    def wrapped_with_session(self, args, context, info):
        session = context['request']['session']
        return fn(self, args, context, info, session)

    return wrapped_with_session


def node_connection_field(query_class, leaf_class, node_fields, description):
    """ Make a ConnectionField for a model class

    :param query_class: query class for model
    :param leaf_class: simple ObjectType
    :param node_fields: list of Fields
    :param description: string describing the collection
    :return: ConnectionField
    """
    entity_name = query_class.__name__

    # node_class is based on the Leaf class but may include collections
    # of related objects; results can also be paged, filtered and sorted
    node_class = type(
        # e.g. AccountNode
        '{}Node'.format(entity_name),
        # inherit from the leaf class
        (leaf_class,),
        # equivalent to
        # class Meta:
        #   interfaces = (Node,)
        #   local_fields = node_fields
        {'Meta': type('Meta', (object,), {
            'interfaces': (Node,),
            'local_fields': node_fields
        })}
    )

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

    return ConnectionField(
        connection_class,
        resolver=resolver,
        description=description
    )


def _replace_object_ids_with_references(model_class, input_dict, context, info):
    """ Before the object model can be updated referenced objects need to be
        looked up. Modifies input dict in place.

    :param model_class: model class being exposed
    :param input_dict: dict of input values
    :param context: passed through
    :param info: passed through
    """
    for reference in references_from(model_class):
        fieldname = reference.source_field_public_name
        if fieldname in input_dict:
            id_ = input_dict.pop(fieldname)
            input_dict[fieldname] = graphene.Node.get_node_from_global_id(id_, context, info)


def _replace_references_with_ids(model_class, fields):
    """ Mutations take IDs rather than object references
        Put ID fields in place of any object references

    :param fields: list of fields
    :param model_class: model class being exposed
    :return: copy of input list with replacements
    """
    modified_fields = fields.copy()
    for reference in references_from(model_class):
        fieldname = reference.source_field_public_name
        modified_fields[fieldname] = graphene.ID(fieldname)
    return modified_fields


def get_create_mutation(model_class, input_fields, leaf_class):
    """ Make a Mutation which can create an entity

    :param model_class: model class being exposed
    :param input_fields: list of Fields
    :param leaf_class: simple ObjectType for model class
    :return: Mutation
    """
    entity_name = model_class.__name__
    field_name = entity_name.lower()

    modified_field_list = _replace_references_with_ids(model_class, input_fields)

    class CreateLeaf(ClientIDMutation):

        @classmethod
        @with_session
        def mutate_and_get_payload(cls, input_dict, context, info, session):
            # use ids in payload to lookup related entities
            _replace_object_ids_with_references(model_class, input_dict, context, info)
            # construct new instance from input
            instance = model_class(**input_dict)
            # tag for persisting
            session.add(instance)
            # must be passed as a kwarg with a name that matches the schema
            tagged_instance = {field_name: instance}
            return cls(**tagged_instance)

    return type(
        # produces a class like:
        # class FundCreateLeaf(CreateLeaf):
        #   class Input:
        #       name = graphene.String('name')
        #       ...
        #   fund = graphene.Field(FundLeaf)
        '{}CreateLeaf'.format(entity_name),
        (CreateLeaf,),
        {
            'Input': type('Input', (object,), modified_field_list),
            field_name: graphene.Field(leaf_class),
            'errors': graphene.List(graphene.String)
        }
    )


def get_update_mutation(model_class, input_fields, leaf_class):
    """ Make a Mutation which can update an entity

    :param model_class: model class being exposed
    :param input_fields: list of Fields
    :param leaf_class: simple ObjectType for model class
    :return: Mutation
    """
    entity_name = model_class.__name__
    field_name = entity_name.lower()

    modified_field_list = _replace_references_with_ids(model_class, input_fields)
    # include internal id with other fields
    modified_field_list[ID_FIELD_NAME] = graphene.ID(ID_FIELD_NAME, required=True)

    class UpdateLeaf(ClientIDMutation):

        @classmethod
        def mutate_and_get_payload(cls, input_dict, context, info):
            # get the id
            id_ = input_dict.pop(ID_FIELD_NAME)
            # lookup the entity
            instance = graphene.Node.get_node_from_global_id(id_, context, info)
            # use ids in payload to lookup related entities
            _replace_object_ids_with_references(model_class, input_dict, context, info)
            # assign properties from input
            for name, value in input_dict.items():
                setattr(instance, name, value)
            # must be passed as a kwarg with a name that matches the schema
            tagged_instance = {field_name: instance}
            return cls(**tagged_instance)

    return type(
        # produces a class like:
        # class FundUpdateLeaf(UpdateLeaf):
        #   class Input:
        #       name = graphene.String('name')
        #       ...
        #   fund = graphene.Field(FundLeaf)
        '{}UpdateLeaf'.format(entity_name),
        (UpdateLeaf,),
        {
            'Input': type('Input', (object,), modified_field_list),
            field_name: graphene.Field(leaf_class),
            'errors': graphene.List(graphene.String)
        }
    )
