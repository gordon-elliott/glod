__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from graphene.relay import Node

from glod.api.account_node import accounts_connection_field, CreateAccountLeaf, UpdateAccountLeaf
from glod.api.fund_node import funds_connection_field, CreateFundLeaf, UpdateFundLeaf
from glod.api.nominal_account_node import nominal_accounts_connection_field, CreateNominalAccountLeaf, UpdateNominalAccountLeaf
from glod.api.subject_node import subjects_connection_field, CreateSubjectLeaf, UpdateSubjectLeaf
from glod.api.parishioner_node import parishioners_connection_field, CreateParishionerLeaf, UpdateParishionerLeaf


class RootQueryType(graphene.ObjectType):
    """ Root query for entity lists which support paging
    """
    node = Node.Field()
    accounts = accounts_connection_field
    funds = funds_connection_field
    nominal_accounts = nominal_accounts_connection_field
    subjects = subjects_connection_field
    parishioners = parishioners_connection_field

    # TODO start here
    # account = account_lookup
    # ....

class Mutations(graphene.ObjectType):
    account_create = CreateAccountLeaf.Field()
    account_update = UpdateAccountLeaf.Field()
    fund_create = CreateFundLeaf.Field()
    fund_update = UpdateFundLeaf.Field()
    nominal_account_create = CreateNominalAccountLeaf.Field()
    nominal_account_update = UpdateNominalAccountLeaf.Field()
    parishioner_create = CreateParishionerLeaf.Field()
    parishioner_update = UpdateParishionerLeaf.Field()
    subject_create = CreateSubjectLeaf.Field()
    subject_update = UpdateSubjectLeaf.Field()


schema = graphene.Schema(query=RootQueryType, mutation=Mutations)
