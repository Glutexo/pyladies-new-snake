from snake.gui import init
from snake.logic import Board, BoardSize, Events, State

__all__ = ["run"]

_BOARD_SIZE = (9, 9)
_INITIAL_SNAKE_SPEED = 1 / 2


def run():
    board = Board(BoardSize(*_BOARD_SIZE))
    state = State.initial(board)
    events = Events(board)
    init(board, _INITIAL_SNAKE_SPEED, state, events)
