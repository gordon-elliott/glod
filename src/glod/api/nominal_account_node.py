__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.api import (
    node_class,
    node_connection_field,
    get_update_mutation,
    get_create_mutation,
    get_local_fields
)
from glod.api.nominal_account_leaf import NominalAccountLeaf
from glod.db.nominal_account import NominalAccount, NominalAccountQuery


nominal_account_fields = get_local_fields(NominalAccount)

NominalAccountNode = node_class(NominalAccount.__name__, NominalAccountLeaf, nominal_account_fields)

nominal_accounts_connection_field = node_connection_field(
    NominalAccount,
    NominalAccountQuery,
    NominalAccountNode,
    description='List of all nominal accounts'
)

nominal_accounts_options_field = node_connection_field(
    NominalAccount,
    NominalAccountQuery,
    NominalAccountLeaf,
    description='List of all nominal accounts for Select fields'
)

CreateNominalAccountLeaf = get_create_mutation(NominalAccount, nominal_account_fields, NominalAccountLeaf)
UpdateNominalAccountLeaf = get_update_mutation(NominalAccount, nominal_account_fields, NominalAccountLeaf)
