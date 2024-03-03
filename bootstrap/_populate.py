"""Controls the order in which tables are populated with data."""

import re
import typing
import asyncpg  # type: ignore
from .generators import game

__all__ = [
    'populate_all',
]

_REGEX_VALID_IDENTIFIER = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*\.?[A-Za-z0-9_]+$')


async def populate_all(conn: asyncpg.Connection, service_id: str) -> None:
    """Populate the database with all available data.

    Args:
        conn (asyncpg.Connection): The connection to the database.
        service_id (str): Census API service ID when retrieving raw data.

    """
    # NOTE: This function controls the order in which tables are populated,
    # which is important due to foreign key constraints.
    data = await game.generate_factions(service_id=service_id)
    await _populate('game.faction', conn, data)
    data = await game.generate_worlds(service_id=service_id)
    await _populate('game.world', conn, data)
    data = await game.generate_zones(service_id=service_id)
    await _populate('game.zone', conn, data)
    data = game.generate_outfit_resources()
    await _populate('game.outfit_resource', conn, data)
    data = await game.generate_facility_types(service_id=service_id)
    await _populate('game.facility_type', conn, data)
    data = await game.generate_facility(service_id=service_id)
    await _populate('game.facility', conn, data)
    data = await game.generate_map_region(service_id=service_id)
    await _populate('game.map_region', conn, data)
    data = await game.generate_lattice_links(service_id=service_id)
    await _populate('game.lattice_link', conn, data, skip_bad_fk=True)


async def _populate(table: str, conn: asyncpg.Connection,
                    data: list[dict[str, typing.Any]], skip_bad_fk: bool = False) -> None:
    """Populate the database with the given data.

    Args:
        table (str): The table (including schema) to populate.
        conn (asyncpg.Connection): The connection to the database.
        data (list): The data to insert into the database.
        skip_bad_fk (bool): Whether to skip rows with FK errors.

    """
    # NOTE (leonhard-s): Because we need to parametrize the table and columns, we cannot use the
    # standard query parameterization features. Instead, we verify that the table and column names
    # are valid and then use string interpolation to build the SQL query with placeholders.

    if not _REGEX_VALID_IDENTIFIER.match(table):
        raise ValueError(f'Invalid table name: {table}')
    columns = data[0].keys()
    if not all(_REGEX_VALID_IDENTIFIER.match(column) for column in columns):
        raise ValueError(f'Invalid column name in table {table}')

    columns = ', '.join(columns)
    placeholders = ', '.join((f'${i+1}' for i, _ in enumerate(data[0])))
    sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'

    print(f'Populating table \'{table}\'...')
    for item in data:
        try:
            await conn.execute(sql, *item.values())  # type: ignore
        except asyncpg.exceptions.UniqueViolationError:
            pass
        except asyncpg.exceptions.ForeignKeyViolationError:
            if skip_bad_fk:
                pass
            else:
                raise
