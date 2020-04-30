from enum import Enum

from os.path import join

__all__ = ("Resources", "resource_path")

_RESOURCES_PATH = "resources"


class Resources(Enum):
    snake = "tail-head.png"
    food = "apple.png"


def resource_path(path):
    return join(_RESOURCES_PATH, path)
