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


class _Sprites(namedtuple("_Sprites", ("snake", "food"))):
    @staticmethod
    def _position_sprite(sprite, pos):
        sprite.x, sprite.y = _tiles_to_pixels(pos)

    @classmethod
    def empty(cls):
        return cls([], None)

    def draw(self):
        for sprite in self._all():
            sprite.draw()

    def update(self, state, images):
        sprites = self._ensure(state, images)
        sprites.position(state)
        return sprites

    def position(self, state):
        snake = zip(self.snake, state.snake)
        food = ((self.food, state.food),)
        for sprite, pos in chain(snake, food):
            self._position_sprite(sprite, pos)

    def _ensure(self, state, images):
        sprites_to_add = []
        num_sprites_to_add = len(state.snake) - len(self.snake)
        if num_sprites_to_add > 0:  # _Snake can only grow. No need to handle negatives.
            sprites_to_add.append(Sprite(images.snake))

        snake = self.snake + sprites_to_add
        food = self.food or Sprite(images.food)

        return _Sprites(snake, food)

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
        self._sprites = _Sprites.empty()

    def clear(self):
        self._window.clear()

    def draw_sprites(self):
        self._sprites.draw()

    def update_sprites(self, updated_state, images):
        self._sprites = self._sprites.update(updated_state, images)

    def bind_events(self, on_draw, on_key_press):
        self._window.push_handlers(on_draw=on_draw, on_key_press=on_key_press)


class _EventBinding:
    def __init__(self, window, images):
        self.binding = {}
        self.window = window
        self.images = images

    def bind(self, event_creator):
        def binding(*args, **kwargs):
            updated_state = self.binding[event_creator](*args, **kwargs)
            self.state_changed(updated_state)

        self.binding[event_creator] = None
        return binding

    def state_changed(self, updated_state):
        self.window.update_sprites(updated_state, self.images)
        self._update_binding(updated_state)

    def _update_binding(self, updated_state):
        for event_creator in self.binding:
            self.binding[event_creator] = event_creator(updated_state)


def _tiles_to_pixels(tiles):
    pixels_x = tiles.x * _TILE_SIZE.x
    pixels_y = tiles.y * _TILE_SIZE.y
    return _Pixels(x=pixels_x, y=pixels_y)


class _EventCreator:
    def __init__(self, window, logic_events):
        self.window = window
        self.logic_events = logic_events

    def interval(self, current_state):
        def interval(dt):
            return self.logic_events.tick(current_state)

        return interval

    def draw(self):
        def draw():
            self.window.clear()
            self.window.draw_sprites()

        return draw

    def on_key_press(self, current_state):
        def on_key_press(symbol, modifier):
            try:
                logic_event = getattr(self.logic_events, _KEY_MAPPING[symbol])
            except KeyError:
                return current_state
            else:
                return logic_event(current_state)

        return on_key_press


def init(board, snake_speed, initial_state, logic_events):
    window = _Window(board)
    images = _Images()
    binding = _EventBinding(window, images)
    creator = _EventCreator(window, logic_events)

    window.bind_events(creator.draw(), binding.bind(creator.on_key_press))

    schedule_interval(binding.bind(creator.interval), snake_speed)

    binding.state_changed(initial_state)
    run()
