from math import floor
from snake.state import State


__all__ = ["initial_state", "tick", "turn"]


_initial_direction = 1, 0


class Collision(RuntimeError):
    pass


class CollisionWithWall(Collision):
    pass


def _dimension_center(dimension):
    return floor(dimension / 2)


def _board_center(board_size):
    return tuple(map(_dimension_center, board_size))


def _in_board(board_size, pos):
    in_h = 0 <= pos[0] < board_size[0]
    in_v = 0 <= pos[1] < board_size[1]
    return in_h and in_v


def _initial_snake(board_size):
    return [_board_center(board_size)]


def _move(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def _snake_head(snake):
    return snake[0]


def _move_snake(snake, direction):
    old_snake_head = _snake_head(snake)
    new_snake_head = _move(old_snake_head, direction)
    return [new_snake_head] + snake[:-1]


def _check_collision(board_size, snake):
    if not _in_board(board_size, snake):
        raise CollisionWithWall


def initial_state(board_size):
    return State(
        board_size=board_size,
        snake=_initial_snake(board_size),
        direction=_initial_direction,
    )


def turn(state, direction):
    state.direction = direction


def tick(state):
    state.snake = _move_snake(state.snake, state.direction)
    _check_collision(state.board_size, _snake_head(state.snake))
