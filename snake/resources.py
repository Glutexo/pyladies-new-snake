from enum import Enum

from os.path import join

__all__ = ("Resources", "resource_path")

_RESOURCES_PATH = "resources"


class Resources(Enum):
    snake = "tail-head.png"
    food = "apple.png"


class _ResourcePathBuilder:
    def __init__(self, path):
        self.path = path

    def __call__(self, resource):
        return join(self.path, resource.value)


resource_path = _ResourcePathBuilder(_RESOURCES_PATH)
