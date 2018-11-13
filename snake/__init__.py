from snake.gui import init
from snake.logic import initial_snake

__all__ = ["run"]

_BOARD_SIZE = (9, 9)


def run():
    snake = initial_snake(_BOARD_SIZE)
    init(_BOARD_SIZE, snake)
