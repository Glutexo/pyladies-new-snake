from snake.gui import init
from snake.logic import initial_state, tick

__all__ = ["run"]

_BOARD_SIZE = (9, 9)


def run():
    state = initial_state(_BOARD_SIZE)
    init(_BOARD_SIZE, state, tick)
