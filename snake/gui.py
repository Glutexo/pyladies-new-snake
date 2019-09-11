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

_KEY_MAPPING = {
    UP: "turn_up",
    DOWN: "turn_down",
    LEFT: "turn_left",
    RIGHT: "turn_right",
}


class _Sprites:
    @staticmethod
    def _position_sprite(sprite, pos):
        sprite.x, sprite.y = _tiles_to_pixels(pos)

    def __init__(self):
        self.snake = []
        self.food = None

    def draw(self):
        for sprite in self._all():
            sprite.draw()

    def ensure(self, state, images):
        if len(state.snake) > len(self.snake):
            num_sprites_to_add = len(state.snake) - len(self.snake)
            for _ in range(num_sprites_to_add):
                self.snake.append(Sprite(images.snake))

        # _Snake can only grow. No need to check len(sprites.snake) > len(state.snake).

        if not self.food:
            self.food = Sprite(images.food)

    def position(self, state):
        for i, sprite in enumerate(self.snake):
            self._position_sprite(sprite, state.snake[i])

        self._position_sprite(self.food, state.food)

    def _all(self):
        return chain(self.snake, [self.food])


class _Images:
    def __init__(self):
        self.snake = load(_SNAKE_IMAGE)
        self.food = load(_FOOD_IMAGE)


class _Window:
    def __init__(self, board):
        window_width, window_height = _tiles_to_pixels(board.size)
        self._window = Window(window_width, window_height, "_Snake")

    def clear(self):
        self._window.clear()

    def bind_events(self, on_draw, on_key_press):
        self._window.push_handlers(on_draw=on_draw, on_key_press=on_key_press)


def _tiles_to_pixels(tiles):
    pixels_x = tiles.x * _TILE_SIZE.x
    pixels_y = tiles.y * _TILE_SIZE.y
    return _Pixels(x=pixels_x, y=pixels_y)


def init(board, snake_speed, initial_state, logic_events):
    def create_interval(current_state):
        def interval(dt):
            return logic_events.tick(current_state)

        return interval

    def create_on_key_press(current_state):
        def on_key_press(symbol, modifier):
            try:
                logic_event = getattr(logic_events, _KEY_MAPPING[symbol])
            except KeyError:
                return current_state
            else:
                return logic_event(current_state)

        return on_key_press

    def state_changed(updated_state, sprites, images):
        sprites.ensure(updated_state, images)
        sprites.position(updated_state)

        for event_creator in gui_events:
            gui_events[event_creator] = event_creator(updated_state)

    def create_draw(window, sprites):
        def draw():
            window.clear()
            sprites.draw()
        return draw

    def bind_event(creator, sprites, images):
        def binding(*args, **kwargs):
            updated_state = gui_events[creator](*args, **kwargs)
            state_changed(updated_state, sprites, images)

        gui_events[creator] = None
        return binding

    gui_events = {}

    _sprites = _Sprites()
    _images = _Images()

    _window = _Window(board)
    _window.bind_events(create_draw(_window, _sprites), bind_event(create_on_key_press, _sprites, _images))

    schedule_interval(bind_event(create_interval, _sprites, _images), snake_speed)

    state_changed(initial_state, _sprites, _images)
    run()
