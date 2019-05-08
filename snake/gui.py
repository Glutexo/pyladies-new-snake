from itertools import chain
from os.path import join
from pyglet.app import run
from pyglet.clock import schedule_interval
from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.window import Window
from pyglet.window.key import DOWN, LEFT, RIGHT, UP


__all__ = ["init"]

_TILE_SIZE = (64, 64)
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


def _in_pixels(tiles):
    width = tiles[0] * _TILE_SIZE[0]
    height = tiles[1] * _TILE_SIZE[1]
    return width, height


def _window(board_size):
    window_width, window_height = _in_pixels(board_size)
    return Window(window_width, window_height, "Snake")


def _ensure_sprites(sprites, state, images):
    if len(state.snake) > len(sprites.snake):
        num_sprites_to_add = len(state.snake) - len(sprites.snake)
        for _ in range(num_sprites_to_add):
            sprites.snake.append(Sprite(images.snake))

    # Snake can only grow. No need to check len(sprites.snake) > len(state.snake).

    if not sprites.food:
        sprites.food = Sprite(images.food)


def _position_sprites(sprites, state):
    for i, sprite in enumerate(sprites.snake):
        sprites.snake[i].x, sprites.snake[i].y = _in_pixels(state.snake[i])

    sprites.food.x, sprites.food.y = _in_pixels(state.food)


def init(board_size, snake_speed, state, turn, tick):
    def draw():
        _ensure_sprites(sprites, state, images)
        _position_sprites(sprites, state)

        window.clear()
        for sprite in chain(sprites.snake, [sprites.food]):
            sprite.draw()

    def keypress(symbol, modifiers):
        if symbol == UP:
            turn(state, (0, 1))
        elif symbol == DOWN:
            turn(state, (0, -1))
        elif symbol == LEFT:
            turn(state, (-1, 0))
        elif symbol == RIGHT:
            turn(state, (1, 0))
        else:
            pass

    def interval(dt):
        tick(board_size, state)

    sprites = _Sprites()
    images = _Images()

    window = _window(board_size)
    window.push_handlers(on_draw=draw, on_key_press=keypress)

    schedule_interval(interval, snake_speed)

    run()
