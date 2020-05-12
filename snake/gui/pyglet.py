from collections import namedtuple

from pyglet.image import load
from pyglet.sprite import Sprite

__all__ = ("load_images", "sprite")


_Images = namedtuple("_Images", ("snake", "food"))


def load_images(image_to_resource):
    resources = map(image_to_resource, _Images._fields)
    images = map(load, resources)
    return _Images(*images)


def sprite(image):
    return Sprite(image)
