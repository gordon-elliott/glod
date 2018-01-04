__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from graphene.relay import Node

from glod.api.account_node import AccountNode, accounts_connection_field, accounts_options_field, CreateAccountLeaf, UpdateAccountLeaf
from glod.api.address_node import AddressNode, addresss_connection_field, CreateAddressLeaf, UpdateAddressLeaf
from glod.api.fund_node import FundNode, funds_connection_field, CreateFundLeaf, UpdateFundLeaf
from glod.api.nominal_account_node import NominalAccountNode, nominal_accounts_connection_field, CreateNominalAccountLeaf, UpdateNominalAccountLeaf
from glod.api.organisation_node import OrganisationNode, organisations_connection_field, CreateOrganisationLeaf, UpdateOrganisationLeaf
from glod.api.organisation_address_node import OrganisationAddressNode, organisation_addresss_connection_field, CreateOrganisationAddressLeaf, UpdateOrganisationAddressLeaf
from glod.api.subject_node import SubjectNode, subjects_connection_field, CreateSubjectLeaf, UpdateSubjectLeaf
from glod.api.parishioner_node import ParishionerNode, parishioners_connection_field, CreateParishionerLeaf, UpdateParishionerLeaf
from glod.api.person_node import PersonNode, persons_connection_field, CreatePersonLeaf, UpdatePersonLeaf
from glod.api.pps_node import PPSNode, ppss_connection_field, CreatePPSLeaf, UpdatePPSLeaf
from glod.api.statement_item_node import StatementItemNode, statement_items_connection_field, CreateStatementItemLeaf, UpdateStatementItemLeaf

class RootQueryType(graphene.ObjectType):
    """ Root query for entity lists which support paging
    """
    node = Node.Field()
    accounts = accounts_connection_field
    account_options = accounts_options_field
    account = Node.Field(AccountNode)
    addresses = addresss_connection_field
    address = Node.Field(AddressNode)
    funds = funds_connection_field
    fund = Node.Field(FundNode)
    nominal_accounts = nominal_accounts_connection_field
    nominal_account = Node.Field(NominalAccountNode)
    organisation_addresses = organisation_addresss_connection_field
    organisation_address = Node.Field(OrganisationAddressNode)
    organisations = organisations_connection_field
    organisation = Node.Field(OrganisationNode)
    subjects = subjects_connection_field
    subject = Node.Field(SubjectNode)
    parishioners = parishioners_connection_field
    parishioner = Node.Field(ParishionerNode)
    people = persons_connection_field
    person = Node.Field(PersonNode)
    ppses = ppss_connection_field
    pps = Node.Field(PPSNode)
    statement_items = statement_items_connection_field
    statement_item = Node.Field(StatementItemNode)


class Mutations(graphene.ObjectType):
    account_create = CreateAccountLeaf.Field()
    account_update = UpdateAccountLeaf.Field()
    address_create = CreateAddressLeaf.Field()
    address_update = UpdateAddressLeaf.Field()
    fund_create = CreateFundLeaf.Field()
    fund_update = UpdateFundLeaf.Field()
    nominal_account_create = CreateNominalAccountLeaf.Field()
    nominal_account_update = UpdateNominalAccountLeaf.Field()
    organisation_address_create = CreateOrganisationAddressLeaf.Field()
    organisation_address_update = UpdateOrganisationAddressLeaf.Field()
    organisation_create = CreateOrganisationLeaf.Field()
    organisation_update = UpdateOrganisationLeaf.Field()
    subject_create = CreateSubjectLeaf.Field()
    subject_update = UpdateSubjectLeaf.Field()
    parishioner_create = CreateParishionerLeaf.Field()
    parishioner_update = UpdateParishionerLeaf.Field()
    person_create = CreatePersonLeaf.Field()
    person_update = UpdatePersonLeaf.Field()
    pps_create = CreatePPSLeaf.Field()
    pps_update = UpdatePPSLeaf.Field()
    statement_item_create = CreateStatementItemLeaf.Field()
    statement_item_update = UpdateStatementItemLeaf.Field()


schema = graphene.Schema(query=RootQueryType, mutation=Mutations)
