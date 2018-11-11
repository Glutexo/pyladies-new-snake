from os.path import join
from pyglet.app import run
from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.window import Window


__all__ = ['init']

_TILE_SIZE = (64, 64)
_SNAKE_IMAGE = join('resources', 'green.png')
del join


def in_pixels_factory(tile_size):
    def in_pixels(in_tiles):
        return in_tiles[0] * tile_size[0], in_tiles[1] * tile_size[1]
    return in_pixels


in_pixels = in_pixels_factory(_TILE_SIZE)
del in_pixels_factory, _TILE_SIZE


def create_window_factory(in_pixels, window):
    def create_window(board_size):
        window_width, window_height = in_pixels(board_size)
        return window(window_width, window_height)
    return create_window


create_window = create_window_factory(in_pixels, Window)
del create_window_factory, Window


def create_sprite_factory_factory(sprite):
    def create_sprite_factory(image):
        def create_sprite(*args, **kwargs):
            return sprite(image, *args, **kwargs)
        return create_sprite
    return create_sprite_factory


create_sprite_factory = create_sprite_factory_factory(Sprite)
del create_sprite_factory_factory, Sprite


def draw_factory(window, sprite):
    def draw():
        window.clear()
        sprite.draw()
    return draw


def init_factory(snake_image_file, create_window, load, create_sprite_factory, in_pixels, draw_factory, run):
    def init(board_size, snake_pos):
        window = create_window(board_size)

        snake_image_resource = load(snake_image_file)
        create_snake_sprite = create_sprite_factory(snake_image_resource)
        x, y = in_pixels(snake_pos)
        snake_sprite = create_snake_sprite(x=x, y=y)

        draw = draw_factory(window, snake_sprite)
        window.push_handlers(on_draw=draw)

        run()
    return init


init = init_factory(_SNAKE_IMAGE, create_window, load, create_sprite_factory, in_pixels, draw_factory, run)
del init_factory, _SNAKE_IMAGE, create_window, load, create_sprite_factory, in_pixels, draw_factory, run
