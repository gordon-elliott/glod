__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import graphene

from a_tuin.api import node_class
from a_tuin.unittests.api.fixtures.models import AClass
from a_tuin.unittests.api.fixtures.leaves import aclass_fields, AClassLeaf, AReferringClassLeaf


aclass_node_fields = aclass_fields.copy()

aclass_node_fields['refers'] = graphene.Field(
    graphene.List(AReferringClassLeaf)
)

AClassNode = node_class(AClass.__name__, AClassLeaf, aclass_node_fields)
