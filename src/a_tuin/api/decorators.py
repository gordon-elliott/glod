__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import logging

from a_tuin.constants import SESSION, EXCEPTIONS_TRAPPED
from a_tuin.metadata.exceptions import FieldErrors


LOG = logging.getLogger(__name__)


def with_session(fn):
    def wrapped_with_session(self, info, **kwargs):
        context = info.context
        session = context['request'][SESSION]
        return fn(self, kwargs, context, info, session)

    return wrapped_with_session


def id_with_session(fn):
    def wrapped_with_session(self, info, _id):
        context = info.context
        session = context['request'][SESSION]
        return fn(self, _id, context, info, session)

    return wrapped_with_session


def handle_field_errors(fn):
    def handling_field_errors(cls, root, info, **input_dict):
        request = info.context['request']
        try:
            request[EXCEPTIONS_TRAPPED] = False
            return fn(cls, root, info, **input_dict)
        except FieldErrors as fe:
            LOG.exception(fe)
            request[EXCEPTIONS_TRAPPED] = {(info.field_name): dict(errors=fe.errors)}
        except Exception as exc:
            LOG.exception(exc)
            request[EXCEPTIONS_TRAPPED] = {(info.field_name): dict(errors=['__all__', str(exc)])}

    return handling_field_errors
