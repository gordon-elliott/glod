__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.api import (
    node_class,
    node_connection_field,
    get_update_mutation,
    get_create_mutation
)
from glod.api.nominal_account_leaf import NominalAccountLeaf, nominal_account_fields
from glod.db.nominal_account import NominalAccount, NominalAccountQuery


NominalAccountNode = node_class(NominalAccount.__name__, NominalAccountLeaf, nominal_account_fields)

nominal_accounts_connection_field = node_connection_field(
    NominalAccount,
    NominalAccountQuery,
    NominalAccountNode,
    description='List of all nominal accounts'
)
CreateNominalAccountLeaf = get_create_mutation(NominalAccount, nominal_account_fields, NominalAccountLeaf)
UpdateNominalAccountLeaf = get_update_mutation(NominalAccount, nominal_account_fields, NominalAccountLeaf)
