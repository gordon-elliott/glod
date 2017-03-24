__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from glod.db.mapper import do_map, db_columns_from_model, db_constraints_from_model
from glod.model.account import Account

columns = db_columns_from_model(Account)
constraints = db_constraints_from_model(Account)

do_map(Account, 'account', columns, constraints)
