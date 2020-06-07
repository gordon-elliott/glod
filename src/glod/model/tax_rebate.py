__copyright__ = 'Copyright(c) Gordon Elliott 2020'

""" 
"""


from a_tuin.metadata import (
    ObjectFieldGroupBase,
    StringField,
    ObjectReferenceField,
    Collection
)


class TaxRebate(ObjectFieldGroupBase):
    # Data usage
    #
    # Record of the years in which a person's PPS was submitted in a rebate claim

    public_interface = (
        ObjectReferenceField('person'),
        StringField('status'),
        StringField('2015_rebate'),
        StringField('2016_rebate'),
        StringField('2017_rebate'),
        StringField('2018_rebate'),
    )

    def has_rebate_for_year(self, fy: int):
        field_name = f"{fy}_rebate"
        if hasattr(self, field_name):
            fy_info = getattr(self, field_name)
            if "claimed" in fy_info:
                filing_year = int(fy_info.replace(" - claimed", ""))
                return filing_year
        return None


class TaxRebateCollection(Collection):
    pass
