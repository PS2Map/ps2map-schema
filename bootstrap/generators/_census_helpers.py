import json
import pathlib
import typing

import aiohttp

__all__ = [
    'get_census_data',
    'patch_census_data',
]

_CENSUS_API_URL = 'https://census.daybreakgames.com'
_PATCH_FILES = pathlib.Path(__file__).parents[2] / 'census_patches'


async def get_census_data(collection: str, service_id: str, game: str | None = None) -> list[dict[str, typing.Any]]:
    """Retrieve raw data from the Census API.
    
    Args:
        collection (str): The collection to retrieve.
        service_id (str): The Census API service ID.
    
    Returns:
        list: The raw data from the Census API.

    """
    if game is None:
        game = 'ps2:v2'
    print(f'Retrieving data for \'{game}/{collection}\'...')
    url = (f'{_CENSUS_API_URL}/{service_id}/get/{game}/'
           f'{collection}?c:limit=10000&c:lang=en')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                data = await response.json()
            except aiohttp.ContentTypeError:
                data = json.loads(await response.text())
    raw_census = data[f'{collection}_list']
    return patch_census_data(collection, raw_census)


def patch_census_data(collection: str, raw_data: list[dict[str, typing.Any]]) -> list[dict[str, typing.Any]]:
    """Patch the raw data from the Census API.

    Some collections are outdated or miss data which is brought in
    from a JSON file here.

    Args:
        collection (str): The collection of data to patch.
        raw_data (list): The raw data from the Census API.
        key (Callable): The field in the dictionary to use as a key
            in the patch file. Defaults to <collection>_id.

    Returns:
        list: The patched data.

    """
    def id_field(data: dict[str, typing.Any]) -> str:
        return data[f'{collection}_id']

    if (_PATCH_FILES / f'{collection}.json').exists():
        print(f'Patching \'{collection}\' data...')
        with open(_PATCH_FILES / f'{collection}.json', 'r', encoding='utf8') as file_:
            patch_file = json.load(file_)
        patched_data: list[dict[str, typing.Any]] = list(raw_data)
        for entry in patched_data:
            patch = patch_file.get(id_field(entry), {})
            entry.update(patch)
        return patched_data
    return raw_data
