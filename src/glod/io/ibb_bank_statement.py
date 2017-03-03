__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from csv import reader

from glod.metadata import StringField, UnusedField, ListFieldGroup, Mapping, prefix_name_with_underscore

statement_item_csv_fields = ListFieldGroup(
    (
        StringField('account'),
        UnusedField('_unused_'),
        StringField('date'),
        UnusedField('_unused_'),
        StringField('details'),
        StringField('currency'),
        StringField('debit'),
        StringField('credit'),
        StringField('balance'),
    )
)


class StatementLoader(object):
    def __init__(self, item_instance_class, account_collection):
        self._item_instance_class = item_instance_class
        self._account_collection = account_collection

        csv_fields = (
            field
            for field in statement_item_csv_fields
            if not isinstance(field, UnusedField)
        )
        self.csv_to_constructor = Mapping(
            statement_item_csv_fields,
            item_instance_class.constructor,
            list(
                zip(
                    csv_fields,
                    item_instance_class.constructor
                )
            )
        )

    def _account_header(self, line):
        account_no = line[3]
        self._account = list(self._account_collection.lookup(account_no))[0]
        return None

    def _statement_line(self, line):
        kwargs = self.csv_to_constructor.cast_from(
            [self._account] + line
        )
        return self._item_instance_class(**kwargs)

    def _eof(self, line):
        return None

    LINE_TYPE_MAP = {
        '01': _account_header,
        '02': _statement_line,
        '99': _eof,
    }

    def load_from_statement(self, csv_file):
        for line in reader(csv_file):
            line_type = line[0]
            processor = self.LINE_TYPE_MAP[line_type]
            item_instance = processor(self, line)
            if item_instance:
                yield item_instance
