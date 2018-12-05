from math import floor
from random import randint
from snake.state import State


__all__ = ["initial_state", "tick", "turn"]


_initial_direction = 1, 0


class Collision(RuntimeError):
    pass


class CollisionWithWall(Collision):
    pass


class CollisionWithSnake(Collision):
    pass


def _dimension_center(dimension):
    return floor(dimension / 2)


def _board_center(board_size):
    return tuple(map(_dimension_center, board_size))


def _dimension_random(dimension):
    return randint(0, dimension - 1)


def _board_random(board_size):
    return _dimension_random(board_size[0]), _dimension_random(board_size[1])


def _in_board(board_size, pos):
    in_h = 0 <= pos[0] < board_size[0]
    in_v = 0 <= pos[1] < board_size[1]
    return in_h and in_v


def _in_snake(snake):
    return _snake_head(snake) in _snake_body(snake)


def _initial_snake(board_size):
    # return [(4, 2), (3, 2), (2, 2), (1, 2), (0, 2), (0, 1)]
    return [_board_center(board_size)]


def _move(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def _snake_head(snake):
    return snake[0]


def _snake_body(snake):
    return snake[1:]


def _snake_has_body(snake):
    return len(snake) > 1


def _extend_snake(snake, direction):
    old_snake_head = _snake_head(snake)
    new_snake_head = _move(old_snake_head, direction)
    return [new_snake_head] + snake


def _contract_snake(snake):
    return snake[:-1]


def _check_collision(board_size, snake):
    if not _in_board(board_size, _snake_head(snake)):
        raise CollisionWithWall
    if _in_snake(snake):
        raise CollisionWithSnake


def _opposite_direction(direction):
    return direction[0] * -1, direction[1] * -1


def _new_food(board_size, snake):
    while True:
        food = _board_random(board_size)
        if food not in snake:
            return food


def initial_state(board_size):
    snake = _initial_snake(board_size)
    food = _new_food(board_size, snake)
    return State(
        board_size=board_size, snake=snake, direction=_initial_direction, food=food
    )


def turn(state, direction):
    snake_has_body = _snake_has_body(state.snake)
    goes_backwards = direction == _opposite_direction(state.direction)
    if not (snake_has_body and goes_backwards):
        state.direction = direction


def tick(board_size, state):
    state.snake = _extend_snake(state.snake, state.direction)
    if _snake_head(state.snake) == state.food:
        state.food = _board_random(board_size)
    else:
        state.snake = _contract_snake(state.snake)
    _check_collision(state.board_size, state.snake)
