from collections import namedtuple

__all__ = ("tiles_to_pixels",)

_Pixels = namedtuple("_Pixels", ("x", "y"))
_TILE_SIZE = _Pixels(64, 64)


def tiles_to_pixels(tiles):
    pixels_x = tiles.x * _TILE_SIZE.x
    pixels_y = tiles.y * _TILE_SIZE.y
    return _Pixels(x=pixels_x, y=pixels_y)
