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


_sprites = {"snake": [], "food": None}


def _in_pixels(tiles):
    width = tiles[0] * _TILE_SIZE[0]
    height = tiles[1] * _TILE_SIZE[1]
    return width, height


def _window(board_size):
    window_width, window_height = _in_pixels(board_size)
    return Window(window_width, window_height, "Snake")


def _ensure_sprites(_sprites, state, images):
    if len(state.snake) > len(_sprites["snake"]):
        num_sprites_to_add = len(state.snake) - len(_sprites["snake"])
        for _ in range(num_sprites_to_add):
            _sprites["snake"].append(Sprite(images["snake"]))

    # Snake can only grow. No need to check len(_sprites["snake"]) > len(state.snake).

    if not _sprites["food"]:
        _sprites["food"] = Sprite(images["food"])


def _position_sprites(_sprites, state):
    for i, sprite in enumerate(_sprites["snake"]):
        _sprites["snake"][i].x, _sprites["snake"][i].y = _in_pixels(state.snake[i])

    _sprites["food"].x, _sprites["food"].y = _in_pixels(state.food)


def init(board_size, snake_speed, state, turn, tick):
    def draw():
        _ensure_sprites(_sprites, state, images)
        _position_sprites(_sprites, state)

        window.clear()
        for sprite in chain(_sprites["snake"], [_sprites["food"]]):
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

    images = {
        "snake": load(_SNAKE_IMAGE),
        "food": load(_FOOD_IMAGE)
    }

    window = _window(board_size)
    window.push_handlers(on_draw=draw, on_key_press=keypress)

    schedule_interval(interval, snake_speed)

    run()
