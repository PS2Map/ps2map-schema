import json
import pathlib
import typing

__all__ = [
    'get_static_data',
]

_STATIC_DATA = pathlib.Path(__file__).parents[2] / 'static'


def get_static_data(name: str) -> list[dict[str, typing.Any]]:
    with open(_STATIC_DATA / 'outfit_resources.json', 'r', encoding='utf8') as file_:
        return json.load(file_)
