from itertools import chain

from snake.gui.pyglet import sprite
from snake.gui.tiles import tiles_to_pixels

__all__ = "Sprites"


class Sprites:
    @staticmethod
    def _position_sprite(sprite, pos):
        sprite.x, sprite.y = tiles_to_pixels(pos)

    @classmethod
    def initialize(cls, images):
        return cls(images, [], None)

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

        return Sprites(self._images, snake, food)

    def _all(self):
        return chain(self._snake, [self._food])
