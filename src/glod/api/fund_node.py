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
from glod.api.fund_leaf import FundLeaf
from glod.db.fund import Fund, FundQuery


fund_fields = get_local_fields(Fund)

FundNode = node_class(Fund.__name__, FundLeaf, fund_fields)

funds_connection_field = node_connection_field(
    Fund,
    FundQuery,
    FundNode,
    description='List of all funds'
)

funds_options_field = node_connection_field(
    Fund,
    FundQuery,
    FundLeaf,
    description='List of all funds for Select fields'
)

CreateFundLeaf = get_create_mutation(Fund, fund_fields, FundLeaf)
UpdateFundLeaf = get_update_mutation(Fund, fund_fields, FundLeaf)
