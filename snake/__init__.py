from snake.gui import init
from snake.logic import Events, State, BoardSize

__all__ = ["run"]

_BOARD_SIZE = (9, 9)
_INITIAL_SNAKE_SPEED = 1 / 2


def run():
    board_size = BoardSize(*_BOARD_SIZE)
    state = State.initial(board_size)
    events = Events(board_size)
    init(board_size, _INITIAL_SNAKE_SPEED, state, events)
