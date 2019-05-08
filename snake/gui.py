from collections import namedtuple
from itertools import chain
from os.path import join
from pyglet.app import run
from pyglet.clock import schedule_interval
from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.window import Window
from pyglet.window.key import DOWN, LEFT, RIGHT, UP


__all__ = ["init"]

_Pixels = namedtuple("_Pixels", ("x", "y"))

_TILE_SIZE = _Pixels(64, 64)
_SNAKE_IMAGE = join("resources", "tail-head.png")
_FOOD_IMAGE = join("resources", "apple.png")


class _Sprites:
    def __init__(self):
        self.snake = []
        self.food = None
        

class _Images:
    def __init__(self):
        self.snake = load(_SNAKE_IMAGE)
        self.food = load(_FOOD_IMAGE)


def _tiles_to_pixels(tiles):
    pixels_x = tiles.x * _TILE_SIZE.x
    pixels_y = tiles.y * _TILE_SIZE.y
    return _Pixels(x=pixels_x, y=pixels_y)


def _window(board_size):
    window_width, window_height = _tiles_to_pixels(board_size)
    return Window(window_width, window_height, "Snake")


def _ensure_sprites(sprites, state, images):
    if len(state.snake) > len(sprites.snake):
        num_sprites_to_add = len(state.snake) - len(sprites.snake)
        for _ in range(num_sprites_to_add):
            sprites.snake.append(Sprite(images.snake))

    # Snake can only grow. No need to check len(sprites.snake) > len(state.snake).

    if not sprites.food:
        sprites.food = Sprite(images.food)


def _position_sprite(sprite, pos):
    sprite.x, sprite.y = _tiles_to_pixels(pos)


def _position_sprites(sprites, state):
    for i, sprite in enumerate(sprites.snake):
        _position_sprite(sprite, state.snake[i])

    _position_sprite(sprites.food, state.food)


def init(board_size, snake_speed, state, events):
    def state_changed():
        _ensure_sprites(sprites, state, images)
        _position_sprites(sprites, state)

    def draw():
        window.clear()
        for sprite in chain(sprites.snake, [sprites.food]):
            sprite.draw()

    def keypress(symbol, modifiers):
        if symbol == UP:
            events.turn_up(state, state_changed)
        elif symbol == DOWN:
            events.turn_down(state, state_changed)
        elif symbol == LEFT:
            events.turn_left(state, state_changed)
        elif symbol == RIGHT:
            events.turn_right(state, state_changed)
        else:
            pass

    def interval(dt):
        events.tick(board_size, state, state_changed)

    sprites = _Sprites()
    images = _Images()

    window = _window(board_size)
    window.push_handlers(on_draw=draw, on_key_press=keypress)

    schedule_interval(interval, snake_speed)
    state_changed()

    run()
