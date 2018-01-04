__copyright__ = 'Copyright(c) Gordon Elliott 2018'

""" 
"""

import graphene

from a_tuin.api import id_with_session, OBJECT_REFERENCE_MAP, leaf_class_interfaces
from glod.db.person import Person, PersonInstanceQuery


class PersonLeaf(graphene.ObjectType):
    class Meta:
        interfaces = leaf_class_interfaces(Person)

    @classmethod
    @id_with_session
    def get_node(cls, id_, context, info, session):
        return PersonInstanceQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['person'] = PersonLeaf
