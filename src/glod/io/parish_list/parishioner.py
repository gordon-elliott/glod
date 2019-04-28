__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.io.gsheet_integration import model_instances
from a_tuin.metadata import Mapping, UnusedField, IntField, StringField, ListFieldGroup

from glod.db.parish_list.parishioner import Parishioner


def parishioners_from_gsheet(session, extract_from_parish_list):

    gs_field_id = IntField('id')
    gs_field_surname = StringField('SURNAME')
    gs_field_first_name = StringField('FIRST_NAME')
    gs_field_title = StringField('TITLE')
    gs_field_status = StringField('STATUS')
    gs_field_main_contact = StringField('main_contact')
    gs_field_household_ref_no = IntField('household_id')
    gs_field_mobile = StringField('mobile')
    gs_field_other_personal = StringField('other personal')
    gs_field_email = StringField('email')
    gs_field_gdpr_response = StringField('gdpr response?')
    gs_field_by_email = StringField('email?')
    gs_field_by_phone = StringField('phone?')
    gs_field_by_post = StringField('post?')
    gs_field_news = StringField('news?')
    gs_field_finance = StringField('finance?')

    parishioner_gsheet = ListFieldGroup(
        (
            gs_field_id,
            gs_field_surname,
            gs_field_first_name,
            gs_field_title,
            gs_field_status,
            gs_field_main_contact,
            gs_field_household_ref_no,
            UnusedField('ADDRESS1'),
            UnusedField('ADDRESS2'),
            UnusedField('ADDRESS3'),
            UnusedField('County'),
            UnusedField('EIRCODE'),
            UnusedField('TELEPHONE'),
            gs_field_mobile,
            gs_field_other_personal,
            gs_field_email,
            gs_field_gdpr_response,
            gs_field_by_email,
            gs_field_by_phone,
            gs_field_by_post,
            gs_field_news,
            gs_field_finance,
        )
    )

    field_mappings = tuple(zip(
        (
            gs_field_id,
            gs_field_surname,
            gs_field_first_name,
            gs_field_title,
            gs_field_status,
            gs_field_main_contact,
            gs_field_household_ref_no,
            gs_field_mobile,
            gs_field_other_personal,
            gs_field_email,
            gs_field_gdpr_response,
            gs_field_by_email,
            gs_field_by_phone,
            gs_field_by_post,
            gs_field_news,
            gs_field_finance,
        ),
        Parishioner.constructor_parameters
    ))

    parishioner_mapping = Mapping(parishioner_gsheet, Parishioner.constructor_parameters, field_mappings)
    parishioner_rows = extract_from_parish_list(
        'parishioners',
        'A1',
        ('id', 'SURNAME', 'FIRST_NAME', 'TITLE', 'STATUS', 'main contact?', 'household id', 'ADDRESS1', 'ADDRESS2', 'ADDRESS3', 'County', 'EIRCODE', 'landline', 'mobile', 'other personal', 'email', 'gdpr response?', 'email?', 'phone?', 'post?', 'news?', 'finance?')
    )
    parishioners = list(model_instances(parishioner_rows, parishioner_mapping, Parishioner))
    session.add_all(parishioners)
