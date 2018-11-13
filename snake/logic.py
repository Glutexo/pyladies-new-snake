from math import floor
from snake.state import State


__all__ = ["initial_state"]


_initial_direction = 0, 0


def _dimension_center(dimension):
    return floor(dimension / 2)


def _board_center(board_size):
    return tuple(map(_dimension_center, board_size))


def _initial_snake(board_size):
    return [_board_center(board_size)]


def initial_state(board_size):
    return State(snake=_initial_snake(board_size), direction=_initial_direction)
