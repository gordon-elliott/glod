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
from glod.api.counterparty_leaf import CounterpartyLeaf
from glod.db.counterparty import Counterparty, CounterpartyQuery


counterparty_fields = get_local_fields(Counterparty)

CounterpartyNode = node_class(Counterparty.__name__, CounterpartyLeaf, counterparty_fields)

counterparty_connection_field = node_connection_field(
    Counterparty,
    CounterpartyQuery,
    CounterpartyNode,
    description='List of all counterparties'
)

counterparty_options_field = node_connection_field(
    Counterparty,
    CounterpartyQuery,
    CounterpartyLeaf,
    description='List of all counterparties for Select fields'
)

CreateCounterpartyLeaf = get_create_mutation(Counterparty, counterparty_fields, CounterpartyLeaf)
UpdateCounterpartyLeaf = get_update_mutation(Counterparty, counterparty_fields, CounterpartyLeaf)
