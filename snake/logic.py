from math import floor


__all__ = ['initial_snake_pos']


def _center(dimension):
    max = dimension - 1
    return floor(max / 2)


def _board_center(board_size):
    return _center(board_size[0]), _center(board_size[1])


def initial_snake_pos(board_size):
    return _board_center(board_size)
