from pyglet.app import run as pyglet_run
from pyglet.window import Window


__all__ = ['run']

_TILE_SIZE = (64, 64)


def _window_size(board_size, tile_size):
    window_width = board_size[0] * tile_size[0]
    window_height = board_size[1] * tile_size[1]
    return window_width, window_height


def _window(board_size):
    window_width, window_height = _window_size(board_size, _TILE_SIZE)
    return Window(window_width, window_height)


def run(board_size):
    _window(board_size)
    pyglet_run()
