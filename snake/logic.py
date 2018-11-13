from math import floor
from snake.state import State


__all__ = ["initial_state", "tick", "turn"]


_initial_direction = 1, 0


def _dimension_center(dimension):
    return floor(dimension / 2)


def _board_center(board_size):
    return tuple(map(_dimension_center, board_size))


def _initial_snake(board_size):
    return [_board_center(board_size)]


def _move(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def initial_state(board_size):
    return State(snake=_initial_snake(board_size), direction=_initial_direction)


def turn(state, direction):
    state.direction = direction


def tick(state):
    old_snake_pos = state.snake[0]
    new_snake_pos = _move(old_snake_pos, state.direction)
    state.snake = [new_snake_pos]
