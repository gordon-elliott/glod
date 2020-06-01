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


class TaxRebateCollection(Collection):
    pass
