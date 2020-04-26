__copyright__ = 'Copyright(c) Gordon Elliott 2018'

""" 
"""

from a_tuin.api import (
    node_class,
    node_connection_field,
    get_update_mutation,
    get_create_mutation,
    get_local_fields
)
from glod.api.pps_leaf import PPSLeaf
from glod.db.pps import PPS, PPSQuery


pps_fields = get_local_fields(PPS)

PPSNode = node_class(PPS.__name__, PPSLeaf, pps_fields)

ppss_connection_field = node_connection_field(
    PPS,
    PPSQuery,
    PPSNode,
    description="List of all PPSes"
)

ppss_options_field = node_connection_field(
    PPS,
    PPSQuery,
    PPSLeaf,
    description="List of all PPSes for Select fields"
)

CreatePPSLeaf = get_create_mutation(PPS, pps_fields, PPSLeaf)
UpdatePPSLeaf = get_update_mutation(PPS, pps_fields, PPSLeaf)
