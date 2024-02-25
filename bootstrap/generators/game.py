import json
import typing

from ._census_helpers import get_census_data
from ._static_data import get_static_data

__all__ = [
    'generate_facility',
    'generate_facility_types',
    'generate_factions',
    'generate_lattice_links',
    'generate_map_region',
    'generate_outfit_resources',
    'generate_worlds',
    'generate_zones',
]


async def generate_factions(service_id: str) -> list[dict[str, typing.Any]]:
    census = await get_census_data('faction', service_id)
    return [{
        'id': int(d['faction_id']),
        'name': str(d['name']['en']),
        'tag': str(d['code_tag']),
    } for d in census]


async def generate_worlds(service_id: str) -> list[dict[str, typing.Any]]:
    data: list[dict[str, typing.Any]] = []
    for game in ('ps2:v2', 'ps2ps4us:v2', 'ps2ps4eu:v2'):
        platform = 'ps4' if 'ps4' in game else 'pc'
        census = await get_census_data('world', service_id, game=game)
        data.extend({
            'id': int(d['world_id']),
            'name': str(d['name']['en']),
            'region': str(d['x-region']) if 'x-region' in d else None,
            'platform': str(platform),
        } for d in census)
    return data


async def generate_zones(service_id: str) -> list[dict[str, typing.Any]]:
    census = await get_census_data('zone', service_id)
    return [{
        'id': int(d['zone_id']),
        'name': str(d['name']['en']),
        'description': str(d.get('description', {'en': None})['en']),
        'code': str(d['x-code'], ),
        'geometry_id': int(d['geometry_id']),
        'hex_size': float(d['hex_size']),
        'map_size': int(d.get('x-map_size', 8192)),
        'dynamic': bool(int(d['dynamic'])),
    } for d in census]


def generate_outfit_resources() -> list[dict[str, typing.Any]]:
    return get_static_data('outfit_resources')


async def generate_facility_types(service_id: str) -> list[dict[str, typing.Any]]:
    census = await get_census_data('map_region', service_id)
    return [{
        'id': int(d['facility_type_id']),
        'name': str(d['facility_type'])
    } for d in census if 'facility_type_id' in d]


async def generate_facility(service_id: str) -> list[dict[str, typing.Any]]:
    # Map used to connect custom resource IDs to facilities
    resource_map = {d['id']: d['name'] for d in get_static_data('outfit_resources')}

    def find_resource_id(data: dict[str, typing.Any]) -> int | None:
        if 'capture_reward' in data:
            description = data['capture_reward'].get('description', '')
            for id_, name in resource_map.items():
                if name in description:
                    return id_
        return None

    census = await get_census_data('map_region', service_id)
    return [{
        'id': int(d['facility_id']),
        'name': str(d['facility_name']),
        'type_id': int(d['facility_type_id']),
        'zone_id': int(d['zone_id']),
        'resource_id': find_resource_id(d),
        'resource_capture_amount': float(d.get('capture_reward', {'amount': 0})['amount']),
        'resource_tick_amount': float(d.get('tick_reward', {'amount': 0})['amount']),
    } for d in census if 'facility_type_id' in d]


async def generate_map_region(service_id: str) -> list[dict[str, typing.Any]]:
    census = await get_census_data('map_region', service_id)
    return [{
        'id': int(d['map_region_id']),
        'name': str(d['facility_name']),
        'facility_id': int(d['facility_id']) if 'facility_id' in d else None,
        'zone_id': int(d['zone_id']),
        'map_pos_x': d['x-map_pos_x'] if 'x-map_pos_x' in d else float(d.get('location_z', 0.0)),
        'map_pos_y': d['x-map_pos_y'] if 'x-map_pos_y' in d else float(d.get('location_x', 0.0)),
    } for d in census]


async def generate_lattice_links(service_id: str) -> list[dict[str, typing.Any]]:
    census_data = await get_census_data('facility_link', service_id)
    return [{
        'facility_a_id': int(d['facility_id_a']),
        'facility_b_id': int(d['facility_id_b']),
        'zone_id': int(d['zone_id']),
    } for d in census_data]
