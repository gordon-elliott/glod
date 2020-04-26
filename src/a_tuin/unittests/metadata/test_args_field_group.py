__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""


from unittest import TestCase

from a_tuin.metadata.field import StringField, IntField
from a_tuin.metadata.field_group import DictFieldGroup
from a_tuin.metadata.mapping import Mapping
from a_tuin.metadata.object_field_group_meta import ObjectFieldGroupBase


class Fixture(ObjectFieldGroupBase):

    public_interface = (
        IntField('id', is_mutable=False),
        StringField('purpose'),
        StringField('name'),
        StringField('account_no'),
        StringField('IBAN', use_custom_properties=True),
    )

    def __init__(self, *args, named=None, **kwargs):
        self._named = named

    @property
    def IBAN(self):
        return self._IBAN

    @IBAN.setter
    def IBAN(self, value):
        self._IBAN = 'IBAN:' + value


class TestArgsFieldGroup(TestCase):

    def test_all_args_passed(self):
        named = 'named parameter'
        identity = 2002
        purpose = 'purpose'
        name = 'name'
        account_no = '303820G'

        fixture = Fixture(identity, purpose, named=named, name=name, account_no=account_no)

        self.assertEqual(name, fixture.name)

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
        from_csv = Fixture(named=named, **cast_values)

        self.assertEqual(named, from_csv._named)
        self.assertEqual(identity, from_csv._id)
        self.assertEqual(purpose, from_csv._purpose)
        self.assertEqual(iban, from_csv._IBAN)

    def test_update_from_dict(self):

        named = 'named parameter'
        identity = 83993
        purpose = 'purpose'
        name = 'name'
        acc_no = '38387RR'
        iban = '3038 3093 3030 03'

        initial_values = {
            'id': identity,
            'purpose': purpose,
            'name': name,
        }
        fixture = Fixture(named=named, **initial_values)

        self.assertEqual(named, fixture._named)
        self.assertEqual(identity, fixture._id)
        self.assertEqual(purpose, fixture._purpose)
        self.assertEqual(None, fixture._IBAN)
        self.assertEqual(None, fixture._account_no)

        new_name = 'updated'
        update_values = {
            'id': 88888,        # this update is ignored
            'name': new_name,
            'account_no': acc_no,
            'IBAN': iban,
        }
        fixture.update_from(update_values)

        self.assertEqual(named, fixture._named)
        self.assertEqual(identity, fixture.id)  # id is unchanged
        self.assertEqual(new_name, fixture.name)
        self.assertEqual(purpose, fixture.purpose)
        self.assertEqual(acc_no, fixture.account_no)
        self.assertEqual('IBAN:' + iban, fixture.IBAN)
