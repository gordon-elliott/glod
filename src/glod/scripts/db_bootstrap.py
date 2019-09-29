__copyright__ = 'Copyright(c) Gordon Elliott 2019'

""" Bootstrap the database and a user

    python glod/scripts/db_bootstrap.py glod/config/dev.yaml
"""


import argparse
import logging
import logging.config
import yaml

from dotmap import DotMap
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from a_tuin.db.session_scope import Session, session_scope


CREATE_ROLE_SQL = """
do $do$ begin
    if not exists (select * from pg_catalog.pg_user where usename = '{restricted_user}') then
        create user {restricted_user} with login createdb inherit password '{restricted_password}';
    end if;
end $do$
"""
INSTRUCTIONS = f"""Operational database created. 
Now set sqlalchemy.url = {connection_string} in alembic.ini and run alembic migrations.
(venv) gordon@dev-workstation:~/projects/glod$ PYTHONPATH=./src alembic upgrade head
"""


def create_operational_database(config_file):
    configuration = DotMap(yaml.full_load(config_file))
    logging.config.dictConfig(configuration.logging.toDict())
    logger = logging.getLogger(__file__)

    try:
        config_dict = configuration.db.toDict()
        connection_string = configuration.db.admin_connection.format(**config_dict)

        if database_exists(connection_string):
            logger.info(f"Database {connection_string} already exists.")
        else:
            create_database(connection_string)
            logger.info(f"Created database {connection_string}.")

        engine = create_engine(connection_string, echo=False)
        Session.configure(bind=engine)

        with session_scope() as session:
            session.execute(CREATE_ROLE_SQL.format(**config_dict))
            session.execute("grant all privileges on database {operational_db_name} to {restricted_user}".format(**config_dict))

        logger.info(INSTRUCTIONS)

    except Exception as ex:
        logger.exception(ex)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create database on db server, add schema user.'
    )
    parser.add_argument('config_file', type=argparse.FileType('r'))
    args = parser.parse_args()

    create_operational_database(args.config_file)
