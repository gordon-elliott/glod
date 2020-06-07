__copyright__ = 'Copyright(c) Gordon Elliott 2020'

""" 
"""
import logging

from collections import defaultdict

from a_tuin.in_out.gsheet_integration import load_class
from a_tuin.metadata import Mapping, StringField, IntField, UnusedField, ListFieldGroup

from glod.model.pps import PPSStatus
from glod.db import TaxRebate, PersonQuery, PPS, PersonRebateSubmission


LOG = logging.getLogger(__name__)

TAX_REBATE_TO_PPS_STATUS = {
    "provided": PPSStatus.Provided,
    "GE exempted": PPSStatus.ExcludedByAdmin,
    "not PAYE taxpayer": PPSStatus.NotIncomeTaxPayer,
    "will not complete": PPSStatus.NotProvided,
}

def tax_rebates_from_gsheet(session, extract_from_detailed_ledger):

    gs_field_parishioner_id = IntField('id')
    gs_field_status = StringField('status')
    gs_field_2015_rebate = StringField('2015 rebate')
    gs_field_2016_rebate = StringField('2016 rebate')
    gs_field_2017_rebate = StringField('2017 rebate')
    gs_field_2018_rebate = StringField('2018 rebate')

    tax_rebate_gsheet = ListFieldGroup(
        (
            gs_field_parishioner_id,
            UnusedField('household id'),
            UnusedField('new pps'),
            gs_field_status,
            gs_field_2015_rebate,
            gs_field_2016_rebate,
            gs_field_2017_rebate,
            gs_field_2018_rebate,
        )
    )

    field_mappings = tuple(zip(
        (
            gs_field_parishioner_id,
            gs_field_status,
            gs_field_2015_rebate,
            gs_field_2016_rebate,
            gs_field_2017_rebate,
            gs_field_2018_rebate,
        ),
        TaxRebate.constructor_parameters
    ))

    field_casts = {
        'id': PersonQuery(session).instance_finder('parishioner_reference_no', int),
    }
    tax_rebate_mapping = Mapping(tax_rebate_gsheet, TaxRebate.constructor_parameters, field_mappings, field_casts)
    tax_rebates = extract_from_detailed_ledger(
        'tax rebate responses',
        'A1',
        ('id', 'household id', 'new pps', 'status', '2015 rebate', '2016 rebate', '2017 rebate', '2018 rebate')
    )
    load_class(session, tax_rebates, tax_rebate_mapping, TaxRebate)


def reorganise_tax_rebates(session, organisations, tax_rebate_submissions):

    submissions_by_fy_and_filing = defaultdict(dict)
    for submission in tax_rebate_submissions:
        filing_year = submission.filing_date.year
        submissions_by_fy_and_filing[submission.FY][filing_year] = submission

    for organisation in organisations:
        new_entities = []
        rebate = None
        pps = None
        tax_payer = None
        # find the tax payer
        for person in organisation.people:
            if person.tax_rebates:
                assert len(person.tax_rebates) == 1, f"Unexpectedly found more than one rebate record for {person}"
                rebate = person.tax_rebates[0]
                tax_payer = person if tax_payer is None else tax_payer
            if person.pps_nos:
                assert len(person.pps_nos) == 1, f"Unexpectedly found more than one pps record for {person}"
                pps = person.pps_nos[0]
                tax_payer = person
        # set the pps status and create a PPS record if necessary
        if rebate:
            pps_status = TAX_REBATE_TO_PPS_STATUS[rebate.status]
            if pps:
                pps.status = pps_status
            else:
                assert pps_status not in (PPSStatus.Provided,)
                pps = PPS(
                    tax_payer,
                    pps_status,
                    None
                )
                new_entities.append(pps)
        if tax_payer:
            # turn the rebate records into a series of links to tax rebate submissions
            for rebate in tax_payer.tax_rebates:
                for fy, filing_year_lookup in submissions_by_fy_and_filing.items():
                    rebate_filing_year = rebate.has_rebate_for_year(fy)
                    if rebate_filing_year:
                        submission = filing_year_lookup.get(rebate_filing_year)
                        if submission:
                            pr_link = PersonRebateSubmission(tax_payer, submission)
                            new_entities.append(pr_link)
                        else:
                            LOG.warning(f"No submission found for FY {fy}, filing year {rebate_filing_year}")

        else:
            if pps:
                assert pps.pps and pps.status == PPSStatus.Provided, f"No PPS is invalid. {pps}"

        session.add_all(new_entities)
