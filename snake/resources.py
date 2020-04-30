from enum import Enum

from os.path import join

__all__ = "resource_path"

_RESOURCES_PATH = "resources"


class _Resources(Enum):
    snake = "tail-head.png"
    food = "apple.png"


def _resource_path(path):
    return join(_RESOURCES_PATH, path)


def resource_path(resource):
    return _resource_path(_Resources[resource].value)
