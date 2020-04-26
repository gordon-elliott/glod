__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

import graphene
from graphene import ClientIDMutation

from a_tuin.constants import SESSION
from a_tuin.api import handle_field_errors
from a_tuin.metadata.reference import references_from

ID_FIELD_NAME = 'id'
CLIENT_MUTATION_ID = 'clientMutationId'


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
            input_dict[fieldname] = graphene.Node.get_node_from_global_id(info, id_)


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
    field_name = entity_name[0].lower() + entity_name[1:]

    modified_field_list = _replace_references_with_ids(model_class, input_fields)

    class CreateLeaf(ClientIDMutation):

        @classmethod
        @handle_field_errors
        def mutate_and_get_payload(cls, root, info, **input_dict):
            context = info.context
            session = context['request'][SESSION]
            # extract the 'clientMutationId'
            # TODO work out what to do with this?
            client_id = input_dict.pop(CLIENT_MUTATION_ID)
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
    field_name = entity_name[0].lower() + entity_name[1:]

    modified_field_list = _replace_references_with_ids(model_class, input_fields)
    # include internal id with other fields
    modified_field_list[ID_FIELD_NAME] = graphene.ID(ID_FIELD_NAME, required=True)

    class UpdateLeaf(ClientIDMutation):

        @classmethod
        @handle_field_errors
        def mutate_and_get_payload(cls, root, info, **input_dict):
            context = info.context
            # extract the 'clientMutationId'
            # TODO work out what to do with this?
            client_id = input_dict.pop(CLIENT_MUTATION_ID)
            # get the id
            id_ = input_dict.pop(ID_FIELD_NAME)
            # lookup the entity
            instance = graphene.Node.get_node_from_global_id(info, id_)
            # use ids in payload to lookup related entities
            _replace_object_ids_with_references(model_class, input_dict, context, info)
            # assign properties from input
            instance.update_from(input_dict)
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
