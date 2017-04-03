__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from sqlalchemy import create_engine
from a_tuin.db.session_scope import Session
from glod.configuration import configuration


engine = create_engine(configuration.db.connection_string, echo=True)
Session.configure(bind=engine)
