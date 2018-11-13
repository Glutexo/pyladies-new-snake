from math import floor


__all__ = ["initial_snake"]


def _dimension_center(dimension):
    return floor(dimension / 2)


def _board_center(board_size):
    return tuple(map(_dimension_center, board_size))


def initial_snake(board_size):
    return [_board_center(board_size)]
