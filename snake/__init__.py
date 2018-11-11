from snake.gui import init

__all__ = ['run']

_BOARD_SIZE = (9, 9)


def run():
    init(_BOARD_SIZE)