import typing
import asyncpg
from .generators import game

__all__ = [
    'populate_all',
]

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


async def _populate(table: str, conn: asyncpg.Connection, data: list[dict[str, typing.Any]], skip_bad_fk: bool = False) -> None:
    """Populate the database with the given data.

    Args:
        table (str): The table (including schema) to populate.
        conn (asyncpg.Connection): The connection to the database.
        data (list): The data to insert into the database.
        skip_bad_fk (bool): Whether to skip rows with FK errors.

    """
    print(f'Populating table \'{table}\'...')
    columns = ''
    placeholders = ''
    for index, item in enumerate(data):
        if index == 0:
            columns = ', '.join(item.keys())
            placeholders = ', '.join([f'${i+1}' for i in range(len(item))])
        try:
            await conn.execute(f'INSERT INTO {table} ({columns}) VALUES ({placeholders})', *item.values())
        except asyncpg.exceptions.UniqueViolationError:
            pass
        except asyncpg.exceptions.ForeignKeyViolationError:
            if skip_bad_fk:
                pass
            else:
                raise
