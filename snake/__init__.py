from snake.gui import init
from snake.logic import initial_snake_pos

__all__ = ["run"]

_BOARD_SIZE = (9, 9)


def run():
    snake_pos = initial_snake_pos(_BOARD_SIZE)
    init(_BOARD_SIZE, snake_pos)
