__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from a_tuin.api import (
    node_class,
    node_connection_field,
    get_update_mutation,
    get_create_mutation,
    get_local_fields
)
from glod.api.account_leaf import AccountLeaf
from glod.api.fund_node import FundLeaf
from glod.db.account import Account, AccountQuery


account_fields = get_local_fields(Account)
account_node_fields = account_fields.copy()

# TODO can we derive this from the model references?
account_node_fields['funds'] = graphene.Field(
    graphene.List(FundLeaf, description='Funds for this account.')
)

AccountNode = node_class(Account.__name__, AccountLeaf, account_node_fields)

accounts_connection_field = node_connection_field(
    Account,
    AccountQuery,
    AccountNode,
    description='List of all bank accounts'
)

accounts_options_field = node_connection_field(
    Account,
    AccountQuery,
    AccountLeaf,
    description='List of all bank accounts for select fields'
)

CreateAccountLeaf = get_create_mutation(Account, account_fields, AccountLeaf)
UpdateAccountLeaf = get_update_mutation(Account, account_fields, AccountLeaf)
