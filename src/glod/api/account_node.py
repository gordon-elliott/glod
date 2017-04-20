__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from glod.api.graphene import node_connection_field, get_update_mutation, get_create_mutation

from glod.db.account import Account, AccountQuery
from glod.api.account_leaf import AccountLeaf, account_fields
from glod.api.fund_node import FundLeaf


account_node_fields = account_fields.copy()
# TODO can we derive this from the model references?
account_node_fields['funds'] = graphene.Field(
    graphene.List(FundLeaf, description='Funds for this account.')
)

accounts_connection_field = node_connection_field(
    AccountQuery,
    AccountLeaf,
    account_node_fields,
    description='List of all bank accounts'
)
CreateAccountLeaf = get_create_mutation(Account, account_fields, AccountLeaf)
UpdateAccountLeaf = get_update_mutation(Account, account_fields, AccountLeaf)
