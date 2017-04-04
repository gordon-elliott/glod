__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from sqlalchemy import create_engine
from a_tuin.db.session_scope import Session
from glod.configuration import configuration

connection_string = configuration.db.connection_template.format(configuration.db.default_database_name)
engine = create_engine(connection_string, echo=False)
Session.configure(bind=engine)
