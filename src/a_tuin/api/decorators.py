__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.constants import SESSION


def with_session(fn):
    def wrapped_with_session(self, args, context, info):
        session = context['request'][SESSION]
        return fn(self, args, context, info, session)

    return wrapped_with_session
