from snake.gui import run as gui_run

__all__ = ['run']

_BOARD_SIZE = (8, 8)


def run():
    gui_run(_BOARD_SIZE)