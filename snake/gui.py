from os.path import join
from pyglet.app import run
from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.window import Window


__all__ = ['init']

_TILE_SIZE = (64, 64)
_SNAKE_IMAGE = join('resources', 'green.png')


def _window_size(board_size, tile_size):
    window_width = board_size[0] * tile_size[0]
    window_height = board_size[1] * tile_size[1]
    return window_width, window_height


def _window(board_size):
    window_width, window_height = _window_size(board_size, _TILE_SIZE)
    return Window(window_width, window_height)


def _sprite(image):
    return Sprite(load(image))


def _draw_factory(window, snake_sprite):
    def draw():
        window.clear()
        snake_sprite.draw()
    return draw


def init(board_size):
    window = _window(board_size)
    snake_sprite = _sprite(_SNAKE_IMAGE)
    draw = _draw_factory(window, snake_sprite)
    window.push_handlers(on_draw=draw)
    run()
