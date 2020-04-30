from collections import namedtuple

from pyglet.image import load

__all__ = ("load_all",)


_Images = namedtuple("_Images", ("snake", "food"))


def load_all(image_to_resource):
    resources = map(image_to_resource, _Images._fields)
    images = map(load, resources)
    return _Images(*images)
