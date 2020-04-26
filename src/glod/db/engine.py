__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import logging

from sqlalchemy import create_engine
from a_tuin.db.session_scope import Session
from glod.configuration import configuration


LOG = logging.getLogger(__file__)

connection_string = configuration.db.restricted_connection.format(**configuration.db.toDict())
engine = create_engine(connection_string, echo=False)
Session.configure(bind=engine)

LOG.info(f"Connecting to DB with {connection_string}")
