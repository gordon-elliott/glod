__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from decimal import Decimal
from typing import Sequence
from collections import namedtuple, defaultdict
from sqlalchemy import text, Integer, String, Boolean

from a_tuin.db import RelationMap, TableMap, PagedQuery, InstanceQuery

from glod.model.pps import PPS, PPSCollection
from glod.model.references import pps__person

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP
from glod.db.constants import SCHEMA_NAME
from glod.db import OrganisationQuery, Organisation

TableMap(PPS, SCHEMA_NAME, 'pps', DB_COLUMN_TYPE_MAP, RelationMap(
    pps__person,
    'person._id',
    backref='pps_nos',
    lazy='joined'
))

DONATION_SUBJECT_IDS = (3, 5, 15, 41, 44)
# TODO get subject ids from DB
IS_INCOME = "Income"
IS_ACTIVE = "Active"
IS_PROVIDED = "Provided"

TARGET_HOUSEHOLDS = """
with target_orgs as (
    select o.id, t.\"FY\", sum(t.amount) as total_amt
    from glod.transaction t
             inner join glod.counterparty c on t.counterparty_id = c.id
             inner join glod.organisation o on c.organisation_id = o.id
    where t.\"FY\" in :txn_from_fys
      and t.income_expenditure = :is_income
      and t.subject_id in :donation_subject_ids
      and o.status = :is_active
    group by o.id, t.\"FY\"
    having sum(t.amount) >= :donation_threshold
), excluding_orgs as (
    select pr.organisation_id
    from glod.person pr
    inner join glod.pps ps on pr.id = ps.person_id and ps.status != :is_provided
)
select pr.organisation_id, pr.id as person_id,
       ps.person_id as pps_person_id, ps.pps, ps.name_override,
       cp.is_main_contact
from glod.person pr
    inner join target_orgs tg on pr.organisation_id = tg.id
    left outer join glod.pps ps on pr.id = ps.person_id
    left outer join glod.communication_permission cp on pr.id = cp.person_id
where pr.organisation_id not in (select organisation_id from excluding_orgs)
group by pr.organisation_id, pr.id,
         ps.person_id, ps.pps, ps.name_override, cp.is_main_contact
order by pr.organisation_id
"""

HOUSEHOLD_FIELDS = dict(
    organisation_id=Integer,
    person_id=Integer,
    pps_person_id=Integer,
    pps=String,
    name_override=String,
    is_main_contact=Boolean
)

HouseholdMember = namedtuple('Household', HOUSEHOLD_FIELDS.keys())


class PPSInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(PPS, PPSCollection, session)


class PPSQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(PPS, PPSCollection, session)

    def chy3_completion_targets(
            self,
            txn_from_fys: Sequence[int],
            donation_threshold: Decimal
    ):

        household_members = self._household_members(txn_from_fys, donation_threshold)
        household_ids = set(hh.organisation_id for hh in household_members)
        household_members_by_organisation_id = defaultdict(list)
        for member in household_members:
            household_members_by_organisation_id[member.organisation_id].append(member)

        household_collection = OrganisationQuery(self._session) \
            .joined_load('organisation_addresses') \
            .filter(Organisation._id.in_(household_ids)) \
            .collection()
        household_orgs = {
            household.id: household
            for household in household_collection
        }
        people_lookup = {
            person.id: person
            for organisation in household_orgs.values()
            for person in organisation.people
        }

        selected_people = [
            self._do_lookups(household_id, household_members, household_orgs, people_lookup)
            for household_id, household_members in household_members_by_organisation_id.items()
        ]

        return selected_people

    def _do_lookups(self, household_id, household_members, household_orgs, people_lookup):
        selected_member = self._select_member(household_id, household_members)
        person = people_lookup[selected_member.person_id]
        household_org = household_orgs[household_id]
        address = household_org.organisation_addresses[0].address
        return selected_member, person, household_org, address

    def _select_member(self, household_id, household_members):
        selected_member = None
        for member in household_members:
            if member.pps_person_id:
                selected_member = member
                break
        if not selected_member:
            for member in household_members:
                if member.is_main_contact:
                    selected_member = member
                    break
        assert selected_member, f"No person selected for household {household_id}"
        return selected_member

    def _household_members(self, txn_from_fys, donation_threshold):
        financial_years = tuple(map(str, txn_from_fys))
        target_households = text(TARGET_HOUSEHOLDS).bindparams(
            txn_from_fys=financial_years,
            donation_threshold=donation_threshold,
            donation_subject_ids=DONATION_SUBJECT_IDS,
            is_income=IS_INCOME,
            is_active=IS_ACTIVE,
            is_provided=IS_PROVIDED
        ).columns(**HOUSEHOLD_FIELDS)
        rows = self._session.execute(target_households)
        household_members = [HouseholdMember(*row) for row in rows]
        return household_members
