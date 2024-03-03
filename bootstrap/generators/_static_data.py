"""Helper functions for loading static data not available on the API."""

import json
import pathlib
import typing

__all__ = [
    'get_static_data',
]

_STATIC_DATA = pathlib.Path(__file__).parents[2] / 'static'


def get_static_data(name: str) -> list[dict[str, typing.Any]]:
    """Load static data from the in-repo JSON files."""
    with open(_STATIC_DATA / f'{name}.json', 'r', encoding='utf8') as file_:
        return json.load(file_)
