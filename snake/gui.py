from os.path import join
from pyglet.app import run
from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.window import Window


__all__ = ['init']

_TILE_SIZE = (64, 64)
_SNAKE_IMAGE = join('resources', 'green.png')


def _in_pixels_factory(tile_size):
    def _in_pixels(in_tiles):
        return in_tiles[0] * tile_size[0], in_tiles[1] * tile_size[1]
    return _in_pixels


_in_pixels = _in_pixels_factory(_TILE_SIZE)


def _window(board_size):
    window_width, window_height = _in_pixels(board_size)
    return Window(window_width, window_height)


def _sprite_factory_from_image(image):
    def _sprite_factory(*args, **kwargs):
        return Sprite(image, *args, **kwargs)
    return _sprite_factory


def _draw_factory(window, sprite):
    def draw():
        window.clear()
        sprite.draw()
    return draw


def init(board_size, snake_pos):
    window = _window(board_size)
    snake_sprite_factory = _sprite_factory_from_image(load(_SNAKE_IMAGE))
    x, y = _in_pixels(snake_pos)
    snake_sprite = snake_sprite_factory(x=x, y=y)
    draw = _draw_factory(window, snake_sprite)
    window.push_handlers(on_draw=draw)
    run()
