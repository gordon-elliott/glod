__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from sqlalchemy import create_engine
from a_tuin.db.session_scope import Session
from glod.configuration import configuration

connection_string = configuration.db.restricted_connection.format(configuration.db)
engine = create_engine(connection_string, echo=False)
Session.configure(bind=engine)
