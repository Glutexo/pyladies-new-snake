from os.path import join
from pyglet.app import run
from pyglet.clock import schedule_interval
from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.window import Window
from pyglet.window.key import DOWN, LEFT, RIGHT, UP


__all__ = ["init"]

_TILE_SIZE = (64, 64)
_SNAKE_IMAGE = join("resources", "green.png")


sprites = set()


def _in_pixels(tiles):
    width = tiles[0] * _TILE_SIZE[0]
    height = tiles[1] * _TILE_SIZE[1]
    return width, height


def _window(board_size):
    window_width, window_height = _in_pixels(board_size)
    return Window(window_width, window_height)


def sprite(image, pos):
    x, y = _in_pixels(pos)
    return Sprite(image, x=x, y=y)


def init(board_size, snake_speed, state, turn, tick):
    def snake_to_sprites(snake):
        for pos in snake:
            s = sprite(snake_image, pos)
            sprites.add(s)

    def draw():
        window.clear()
        for sprite in sprites:
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
        tick(state)

        for sprite in list(sprites):
            sprite.delete()
            sprites.remove(sprite)

        snake_to_sprites(state.snake)

    snake_image = load(_SNAKE_IMAGE)
    snake_to_sprites(state.snake)

    window = _window(board_size)
    window.push_handlers(on_draw=draw, on_key_press=keypress)

    schedule_interval(interval, snake_speed)

    run()
