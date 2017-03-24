__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()