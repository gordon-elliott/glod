__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from glod.api.graphene import node_connection_field, get_update_mutation, get_create_mutation

from glod.api.fund_leaf import FundLeaf, fund_fields
from glod.db.fund import Fund, FundQuery


FundNode, funds_connection_field = node_connection_field(
    FundQuery,
    FundLeaf,
    fund_fields,
    description='List of all funds'
)
CreateFundLeaf = get_create_mutation(Fund, fund_fields, FundLeaf)
UpdateFundLeaf = get_update_mutation(Fund, fund_fields, FundLeaf)
