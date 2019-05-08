from collections import namedtuple
from itertools import chain
from os.path import join
from types import MethodType
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
    UP: "turn_up", DOWN: "turn_down", LEFT: "turn_left", RIGHT: "turn_right"
}


class _Sprites:
    def __init__(self):
        self.snake = []
        self.food = None
        

class _Images:
    def __init__(self):
        self.snake = load(_SNAKE_IMAGE)
        self.food = load(_FOOD_IMAGE)


EventTypes = namedtuple("EventTypes", ("interval", "on_key_press"))


class _Events:
    def __init__(self, initial_state, state_changed, event_funcs):
        def event_func(name):
            def event(self, *args, **kwargs):
                updated_state = getattr(self._events, name)(*args, **kwargs)
                state_changed(updated_state)
                self._update_events(updated_state)
            return event

        self._state_changed = state_changed
        self._event_funcs = event_funcs
        self._update_events(initial_state)

        for name in event_funcs._fields:
            method = event_func(name)
            setattr(self, name, MethodType(method, self))

    def _update_events(self, updated_state):
        events = {}
        for name, event_func in self._event_funcs._asdict().items():
            events[name] = event_func(updated_state)
        self._events = EventTypes(**events)

    # def interval(self, dt):
    #     updated_state = self._events.interval(dt)
    #     self._state_changed(updated_state)
    #     self._update_events(updated_state)
    #
    # def on_key_press(self, symbol, modifier):
    #     updated_state = self._events.on_key_press(symbol, modifier)
    #     self._state_changed(updated_state)
    #     self._update_events(updated_state)


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


def init(board_size, snake_speed, initial_state, logic_events):
    def interval_func(current_state):
        def interval(dt):
            return logic_events.tick(board_size, current_state)
        return interval

    def on_key_press_func(current_state):
        def on_key_press(symbol, modifier):
            try:
                event = getattr(logic_events, _KEY_MAPPING[symbol])
            except KeyError:
                pass
            else:
                return event(current_state)
        return on_key_press

    def state_changed(current_state):
        _ensure_sprites(sprites, current_state, images)
        _position_sprites(sprites, current_state)

    def draw():
        window.clear()
        for sprite in chain(sprites.snake, [sprites.food]):
            sprite.draw()

    sprites = _Sprites()
    images = _Images()
    gui_event_types = EventTypes(interval_func, on_key_press_func)
    gui_events = _Events(initial_state, state_changed, gui_event_types)

    window = _window(board_size)
    window.push_handlers(on_draw=draw, on_key_press=gui_events.on_key_press)

    schedule_interval(gui_events.interval, snake_speed)

    state_changed(initial_state)
    run()
