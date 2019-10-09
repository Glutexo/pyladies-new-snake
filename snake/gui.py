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


class _EventBinding:
    def __init__(self, sprites, images):
        self.binding = {}
        self.sprites = sprites
        self.images = images

    def bind(self, event_creator):
        def binding(*args, **kwargs):
            updated_state = self.binding[event_creator](*args, **kwargs)
            self.state_changed(updated_state)

        self.binding[event_creator] = None
        return binding

    def state_changed(self, updated_state):
        self._update_sprites(updated_state)
        self._update_binding(updated_state)

    def _update_sprites(self, updated_state):
        self.sprites.ensure(updated_state, self.images)
        self.sprites.position(updated_state)

    def _update_binding(self, updated_state):
        for event_creator in self.binding:
            self.binding[event_creator] = event_creator(updated_state)


def _tiles_to_pixels(tiles):
    pixels_x = tiles.x * _TILE_SIZE.x
    pixels_y = tiles.y * _TILE_SIZE.y
    return _Pixels(x=pixels_x, y=pixels_y)


def create_draw(window, sprites):
    def draw():
        window.clear()
        sprites.draw()

    return draw


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

    sprites = _Sprites()
    images = _Images()
    binding = _EventBinding(sprites, images)

    window = _Window(board)
    window.bind_events(create_draw(window, sprites), binding.bind(create_on_key_press))

    schedule_interval(binding.bind(create_interval), snake_speed)

    binding.state_changed(initial_state)
    run()
