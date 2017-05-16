__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from graphene.relay import Node

from glod.api.account_node import AccountNode, accounts_connection_field, accounts_options_field, CreateAccountLeaf, UpdateAccountLeaf
from glod.api.fund_node import FundNode, funds_connection_field, CreateFundLeaf, UpdateFundLeaf
from glod.api.nominal_account_node import NominalAccountNode, nominal_accounts_connection_field, CreateNominalAccountLeaf, UpdateNominalAccountLeaf
from glod.api.subject_node import SubjectNode, subjects_connection_field, CreateSubjectLeaf, UpdateSubjectLeaf
from glod.api.parishioner_node import ParishionerNode, parishioners_connection_field, CreateParishionerLeaf, UpdateParishionerLeaf
from glod.api.statement_item_node import StatementItemNode, statement_items_connection_field, CreateStatementItemLeaf, UpdateStatementItemLeaf

class RootQueryType(graphene.ObjectType):
    """ Root query for entity lists which support paging
    """
    node = Node.Field()
    accounts = accounts_connection_field
    account_options = accounts_options_field
    account = Node.Field(AccountNode)
    funds = funds_connection_field
    fund = Node.Field(FundNode)
    nominal_accounts = nominal_accounts_connection_field
    nominal_account = Node.Field(NominalAccountNode)
    subjects = subjects_connection_field
    subject = Node.Field(SubjectNode)
    parishioners = parishioners_connection_field
    parishioner = Node.Field(ParishionerNode)
    statement_items = statement_items_connection_field
    statement_item = Node.Field(StatementItemNode)


class Mutations(graphene.ObjectType):
    account_create = CreateAccountLeaf.Field()
    account_update = UpdateAccountLeaf.Field()
    fund_create = CreateFundLeaf.Field()
    fund_update = UpdateFundLeaf.Field()
    nominal_account_create = CreateNominalAccountLeaf.Field()
    nominal_account_update = UpdateNominalAccountLeaf.Field()
    subject_create = CreateSubjectLeaf.Field()
    subject_update = UpdateSubjectLeaf.Field()
    parishioner_create = CreateParishionerLeaf.Field()
    parishioner_update = UpdateParishionerLeaf.Field()
    statement_item_create = CreateStatementItemLeaf.Field()
    statement_item_update = UpdateStatementItemLeaf.Field()


schema = graphene.Schema(query=RootQueryType, mutation=Mutations)
