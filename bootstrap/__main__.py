import argparse
import asyncio
import os

import asyncpg

from ._populate import populate_all

DEFAULT_DB_HOST = '127.0.0.1'
DEFAULT_DB_PORT = 5432
DEFAULT_DB_NAME = 'PS2Map'
DEFAULT_DB_USER = 'postgres'


async def create_schemas(conn: asyncpg.Connection) -> None:
    """Create the necessary schemas in the database.

    Args:
        conn (asyncpg.Connection): The connection to the database.

    """
    for schema in ('game', 'map_state', 'api'):
        with open(f'schemas/{schema}.sql', 'r', encoding='utf8') as file_:
            sql = file_.read()
        print(f'Creating schema \'{schema}\'...')
        await conn.execute(sql)
    print('Schemas created')


async def async_main(db_host: str, db_port: int, db_user: str, db_pass: str,
                     db_name: str, service_id: str) -> None:
    """Asynchronous script entry point.

    This coroutine acts much like the ``if __name__ == '__main__':``
    clause below, but supports asynchronous methods.

    Args:
        db_host (str): Host address of the database server.
        db_port (str): Port of the database server.
        db_user (str): Login user for the database server.
        db_pass (str): Login password for the database server.
        db_name (str): Name of the database to access.
        service_id (str): Census API service ID when retrieving raw data.

    """
    # Connect to the database
    conn = await asyncpg.connect(host=db_host, port=db_port, user=db_user,
                                 password=db_pass, database=db_name)
    # Set up schemas
    await create_schemas(conn)
    # Populate the database
    await populate_all(conn, service_id)


if __name__ == '__main__':
    # Optionally retrieve default values from environment variables
    _def_service_id = os.getenv('PS2MAP_SERVICE_ID', 's:example')
    _def_db_host = os.getenv('PS2MAP_DB_HOST', DEFAULT_DB_HOST)
    _def_db_port = int(os.getenv('PS2MAP_DB_PORT', str(DEFAULT_DB_PORT)))
    _def_db_name = os.getenv('PS2MAP_DB_NAME', DEFAULT_DB_NAME)
    _def_db_user = os.getenv('PS2MAP_DB_USER', DEFAULT_DB_USER)
    _def_db_pass = os.getenv('PS2MAP_DB_PASS')
    # Define command line arguments
    _parser = argparse.ArgumentParser()
    _parser.add_argument(
        '--db-user', '-U', default=_def_db_user,
        help='The user account to use when connecting to the database')
    _parser.add_argument(
        '--db-pass', '-P', required=_def_db_pass is None, default=_def_db_pass,
        help='The password to use when connecting to the database')
    _parser.add_argument(
        '--db-host', '-H', default=_def_db_host,
        help='The address of the database host')
    _parser.add_argument(
        '--db-port', '-T', default=_def_db_port,
        help='The port of the database host')
    _parser.add_argument(
        '--db-name', '-N', default=_def_db_name,
        help='The name of the database to access')
    _parser.add_argument(
        '--service-id', '-S', default=_def_service_id,
        help='The service ID to use when retrieving data from the Census API')
    # Parse arguments from sys.argv
    _kwargs = vars(_parser.parse_args())
    # Run the main script
    asyncio.run(async_main(**_kwargs))
