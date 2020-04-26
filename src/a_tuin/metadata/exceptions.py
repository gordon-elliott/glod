__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from contextlib import contextmanager


DATA_LOAD_ERRORS = (ArithmeticError, AttributeError, LookupError, TypeError, ValueError)


class FieldAssignmentError(Exception):
    def __init__(self, field, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._field = field

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, value):
        self._field = value

    @property
    def field_name(self):
        return self._field.name

    @property
    def original_exception(self):
        return self.args[0]

    def __str__(self):
        return "{0.field_name}: {0.args}".format(self)


class RequiredValueMissing(FieldAssignmentError):
    pass


class FieldErrors(Exception):
    def __init__(self, field_errors, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._field_errors = field_errors

    @property
    def errors(self):
        error_list = []
        for field_error in self._field_errors:
            error_list.append(field_error.field_name)
            error_list.append(str(field_error.original_exception))

        return error_list

    def __str__(self):
        return "Field Errors\n\t{}".format('\n\t'.join(map(str, self._field_errors)))


@contextmanager
def field_errors_check():
    errors = []

    yield errors

    if errors:
        raise FieldErrors(errors)
