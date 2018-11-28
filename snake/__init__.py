from snake.gui import init
from snake.logic import initial_state, tick, turn

__all__ = ["run"]

_BOARD_SIZE = (9, 9)
_INITIAL_SNAKE_SPEED = 1 / 2


def run():
    state = initial_state(_BOARD_SIZE)
    init(_BOARD_SIZE, _INITIAL_SNAKE_SPEED, state, turn, tick)
