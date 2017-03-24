__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from glod.db.mapper import do_map, db_columns_from_model, db_constraints_from_model, db_fk_from_model
from glod.model.statement_item import StatementItem

fk_fieldname = '_account_id'
object_ref_fieldname = '_account'
fk_column_name = 'account_id'
referenced_pk_fieldname = 'account._id'

columns = db_columns_from_model(StatementItem)
fk_constraint = db_fk_from_model(
    columns,
    fk_fieldname,
    fk_column_name,
    object_ref_fieldname,
    referenced_pk_fieldname
)
fk_constraints = (fk_constraint,)
constraints = db_constraints_from_model(StatementItem, fk_constraints)
do_map(StatementItem, 'statement_item', columns, constraints)

