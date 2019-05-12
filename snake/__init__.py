from snake.gui import init
from snake.logic import Events, initial_state, Tiles

__all__ = ["run"]

_BOARD_SIZE = Tiles(9, 9)
_INITIAL_SNAKE_SPEED = 1 / 2


def run():
    state = initial_state(_BOARD_SIZE)
    events = Events(_BOARD_SIZE)
    init(_BOARD_SIZE, _INITIAL_SNAKE_SPEED, state, events)
