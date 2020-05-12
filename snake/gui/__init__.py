from collections import namedtuple
from itertools import chain

from pyglet.app import run
from pyglet.clock import schedule_interval
from pyglet.window import Window
from pyglet.window.key import DOWN, LEFT, RIGHT, UP

from snake.gui.pyglet import load_images
from snake.gui.pyglet import sprite
from snake.resources import resource_path

__all__ = ["init"]

_Pixels = namedtuple("_Pixels", ("x", "y"))

_TILE_SIZE = _Pixels(64, 64)

_WINDOW_TITLE = "Snake"

_KEY_MAPPING = {
    UP: "turn_up",
    DOWN: "turn_down",
    LEFT: "turn_left",
    RIGHT: "turn_right",
}


def _load_images():
    return load_images(resource_path)


class _Sprites:
    @staticmethod
    def _position_sprite(sprite, pos):
        sprite.x, sprite.y = _tiles_to_pixels(pos)

    @classmethod
    def initialize(cls):
        return cls(_load_images(), [], None)

    def __init__(self, images, snake, food):
        self._images = images
        self._snake = snake
        self._food = food

    def draw(self):
        for sprite in self._all():
            sprite.draw()

    def update(self, state):
        sprites = self._ensure(state)
        sprites._position(state)
        return sprites

    def _position(self, state):
        snake = zip(self._snake, state.snake)
        food = ((self._food, state.food),)
        for sprite, pos in chain(snake, food):
            self._position_sprite(sprite, pos)

    def _ensure(self, state):
        sprites_to_add = []
        num_sprites_to_add = len(state.snake) - len(self._snake)
        if num_sprites_to_add > 0:  # _Snake can only grow. No need to handle negatives.
            sprites_to_add.append(sprite(self._images.snake))

        snake = self._snake + sprites_to_add
        food = self._food or sprite(self._images.food)

        return _Sprites(self._images, snake, food)

    def _all(self):
        return chain(self._snake, [self._food])


class _Window:
    @staticmethod
    def _window_size(board_size):
        return _tiles_to_pixels(board_size)

    @classmethod
    def initialize(cls, board):
        window_size = cls._window_size(board.size)
        window = Window(window_size.x, window_size.y, _WINDOW_TITLE)
        sprites = _Sprites.initialize()
        return cls(window, sprites)

    def __init__(self, window, sprites):
        self._window = window
        self._sprites = sprites

    def redraw(self):
        self._clear()
        self._draw_sprites()

    def update_sprites(self, updated_state):
        self._sprites = self._sprites.update(updated_state)

    def bind_events(self, on_draw, on_key_press):
        self._window.push_handlers(on_draw=on_draw, on_key_press=on_key_press)

    def _clear(self):
        self._window.clear()

    def _draw_sprites(self):
        self._sprites.draw()


class _EventBinding:
    @classmethod
    def initialize(cls, window):
        return cls({}, window)

    def __init__(self, binding, window):
        self._binding = binding
        self._window = window

    def bind(self, event_creator):
        def binding(*args, **kwargs):
            updated_state = self._binding[event_creator](*args, **kwargs)
            self.state_changed(updated_state)

        self._binding[event_creator] = None
        return binding

    def state_changed(self, updated_state):
        self._window.update_sprites(updated_state)
        self._update_binding(updated_state)

    def _update_binding(self, updated_state):
        for event_creator in self._binding:
            self._binding[event_creator] = event_creator(updated_state)


def _tiles_to_pixels(tiles):
    pixels_x = tiles.x * _TILE_SIZE.x
    pixels_y = tiles.y * _TILE_SIZE.y
    return _Pixels(x=pixels_x, y=pixels_y)


class _EventCreator:
    def __init__(self, window, logic_events):
        self._window = window
        self._logic_events = logic_events

    def interval(self, current_state):
        def interval(dt):
            return self._logic_events.tick(current_state)

        return interval

    def draw(self):
        def draw():
            self._window.redraw()

        return draw

    def on_key_press(self, current_state):
        def on_key_press(symbol, modifier):
            try:
                logic_event = getattr(self._logic_events, _KEY_MAPPING[symbol])
            except KeyError:
                return current_state
            else:
                return logic_event(current_state)

        return on_key_press


def init(board, snake_speed, initial_state, logic_events):
    window = _Window.initialize(board)
    binding = _EventBinding.initialize(window)
    creator = _EventCreator(window, logic_events)

    window.bind_events(creator.draw(), binding.bind(creator.on_key_press))

    schedule_interval(binding.bind(creator.interval), snake_speed)

    binding.state_changed(initial_state)
    run()
