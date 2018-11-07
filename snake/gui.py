from collections import namedtuple
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


CreateWindowFactoryFunctions = namedtuple('CreateWindowFactoryFunction', ('in_pixels', 'window'))
create_window_factory_functions = CreateWindowFactoryFunctions(in_pixels, Window)
del CreateWindowFactoryFunctions, Window


def create_window_factory(functions):
    def create_window(board_size):
        window_width, window_height = functions.in_pixels(board_size)
        return functions.window(window_width, window_height)
    return create_window


create_window = create_window_factory(create_window_factory_functions)
del create_window_factory, create_window_factory_functions


CreateSpriteFactoryFunctions = namedtuple('CreateSpriteFactoryFunctions', ('sprite',))
create_sprite_factory_functions = CreateSpriteFactoryFunctions(Sprite)
del CreateSpriteFactoryFunctions, Sprite


def create_sprite_factory_factory(functions):
    def create_sprite_factory(image):
        def create_sprite(*args, **kwargs):
            return functions.sprite(image, *args, **kwargs)
        return create_sprite
    return create_sprite_factory


create_sprite_factory = create_sprite_factory_factory(create_sprite_factory_functions)
del create_sprite_factory_factory


def draw_factory(window, sprite):
    def draw():
        window.clear()
        sprite.draw()
    return draw


def init_factory(snake_image_file, functions):
    def init(board_size, snake_pos):
        window = functions.create_window(board_size)

        snake_image_resource = functions.load(snake_image_file)
        create_snake_sprite = functions.create_sprite_factory(snake_image_resource)
        x, y = functions.in_pixels(snake_pos)
        snake_sprite = create_snake_sprite(x=x, y=y)

        draw = functions.draw_factory(window, snake_sprite)
        window.push_handlers(on_draw=draw)

        functions.run()
    return init


InitFunctions = namedtuple('InitFunctions', ('create_window', 'load', 'create_sprite_factory', 'in_pixels', 'draw_factory', 'run'))
del namedtuple
init_functions = InitFunctions(create_window, load, create_sprite_factory, in_pixels, draw_factory, run)
del InitFunctions, create_window, load, create_sprite_factory, in_pixels, draw_factory, run


init = init_factory(_SNAKE_IMAGE, init_functions)
del init_factory, _SNAKE_IMAGE, init_functions
