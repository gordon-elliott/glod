__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from glod.metadata import StringField, IntField, ArgsFieldGroup, ObjectFieldGroupMeta


class Account(object, metaclass=ObjectFieldGroupMeta):

    constructor_parameters = ArgsFieldGroup(
        (
            IntField('id'),
            StringField('purpose'),
            StringField('status'),
            StringField('name'),
            StringField('institution'),
            StringField('sort_code'),
            StringField('account_no'),
            StringField('BIC'),
            StringField('IBAN'),
        )
    )

    # metaclass takes care of dealing with the args
    def __init__(self, *args, **kwargs):
        pass
