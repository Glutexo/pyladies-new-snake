from snake.gui import init

__all__ = ['run']

_BOARD_SIZE = (8, 8)


def run():
    init(_BOARD_SIZE)