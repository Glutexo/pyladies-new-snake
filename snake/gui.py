from os.path import join
from pyglet.app import run
from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.window import Window


__all__ = ["init"]

_TILE_SIZE = (64, 64)
_SNAKE_IMAGE = join("resources", "green.png")


sprites = set()


def _in_pixels(tiles):
    width = tiles[0] * _TILE_SIZE[0]
    height = tiles[1] * _TILE_SIZE[1]
    return width, height


def _window(board_size):
    window_width, window_height = _in_pixels(board_size)
    return Window(window_width, window_height)


def sprite(image, pos):
    x, y = _in_pixels(pos)
    return Sprite(image, x=x, y=y)


def init(board_size, snake_pos):
    def draw():
        window.clear()
        for sprite in sprites:
            sprite.draw()

    snake_image = load(_SNAKE_IMAGE)
    snake_sprite = sprite(snake_image, snake_pos)
    sprites.add(snake_sprite)

    window = _window(board_size)
    window.push_handlers(on_draw=draw)

    run()
