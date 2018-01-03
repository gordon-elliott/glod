__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.metadata import replace_underscore_with_space, ListFieldGroup


def get_gsheet_fields(model_class, renamed_fields):
    gsheet_fields = model_class.constructor_parameters.derive(
        replace_underscore_with_space,
        ListFieldGroup
    )

    if renamed_fields:
        for constructor_field_name, gsheet_column_name in renamed_fields.items():
            gsheet_fields[constructor_field_name].name = gsheet_column_name

    return gsheet_fields


def model_instances(gsheet_rows, gsheet_to_constructor, model_class):
    return (
        model_class(**gsheet_to_constructor.cast_from(row))
        for row in gsheet_rows
    )


def load_class(session, gsheet_rows, gsheet_to_constructor, model_class):
    instances = model_instances(gsheet_rows, gsheet_to_constructor, model_class)
    session.add_all(instances)
