__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""


from unittest import TestCase

from glod.metadata.field import StringField, IntField
from glod.metadata.field_group import DictFieldGroup
from glod.metadata.mapping import Mapping
from glod.metadata.args_field_group import ArgsFieldGroup
from glod.metadata.object_field_group_mixin import ObjectFieldGroupMixin


class Fixture(ObjectFieldGroupMixin):

    public_interface = (
        IntField('id'),
        StringField('purpose'),
        StringField('name'),
        StringField('account_no'),
        StringField('IBAN'),
    )

    constructor_parameters = ArgsFieldGroup(public_interface)

    def __init__(self, named, *args, **kwargs):
        constructor_to_internal = self.map_constructor_to_internal(self.constructor_parameters)
        constructor_to_internal.update_in_place((args, kwargs), self)

        self._named = named


class TestArgsFieldGroup(TestCase):

    def test_all_args_passed(self):
        named = 'named parameter'
        identity = 2002
        purpose = 'purpose'
        name = 'name'
        account_no = '303820G'

        fixture = Fixture(named, identity, purpose, name=name, account_no=account_no)

        self.assertEqual(named, fixture._named)
        self.assertEqual(identity, fixture._id)
        self.assertEqual(purpose, fixture._purpose)
        self.assertEqual(name, fixture._name)
        self.assertEqual(account_no, fixture._account_no)

    def test_cast_from(self):

        csv_fields = DictFieldGroup(Fixture.public_interface)
        csv_to_constructor = Mapping(csv_fields, Fixture.constructor_parameters)

        named = 'named parameter'
        identity = 83993
        purpose = 'purpose'
        name = 'name'
        acc_no = '38387RR'
        iban = 'IBAN 30383093 30 30 03'

        cast_values = csv_to_constructor.cast_from({
            'id': identity,
            'purpose': purpose,
            'name': name,
            'account_no': acc_no,
            'IBAN': iban,
        })
        from_csv = Fixture(named, **cast_values)

        self.assertEqual(named, from_csv._named)
        self.assertEqual(identity, from_csv._id)
        self.assertEqual(purpose, from_csv._purpose)
        self.assertEqual(iban, from_csv._IBAN)
