__copyright__ = 'Copyright(c) Gordon Elliott 2019'

""" 
id	SURNAME	FIRST_NAME	TITLE	STATUS	main contact?	household id	
ADDRESS1	ADDRESS2	ADDRESS3	County	EIRCODE	landline	
mobile	other personal	email	gdpr response?	email?	phone?	post?	news?	finance?
"""

from a_tuin.metadata import IntField, StringField, ObjectFieldGroupBase, Collection


class Parishioner(ObjectFieldGroupBase):
    # Receives parishioner records from parish list

    public_interface = (
        IntField('reference_no', is_mutable=False),
        StringField('surname'),
        StringField('first_name'),
        StringField('title'),
        StringField('status'),
        StringField('main_contact'),
        IntField('household_ref_no'),
        StringField('mobile'),
        StringField('other'),
        StringField('email'),
        StringField('gdpr_response'),
        StringField('by_email'),
        StringField('by_phone'),
        StringField('by_post'),
        StringField('news'),
        StringField('finance'),
    )


class ParishionerCollection(Collection):
    pass
