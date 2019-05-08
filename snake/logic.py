from collections import namedtuple
from enum import Enum
from math import floor
from random import randint
from snake.state import State, tick, turn


__all__ = ["Events", "initial_state", "Tiles"]


Tiles = namedtuple("Tiles", ("x", "y"))

_initial_direction = Tiles(1, 0)


class Collision(RuntimeError):
    pass


class CollisionWithWall(Collision):
    pass


class CollisionWithSnake(Collision):
    pass


def _random(num_tiles):
    return randint(0, num_tiles - 1)


def _center(num_tiles):
    return floor(num_tiles / 2)


def _board_pos(board_size, transformation):
    x = transformation(board_size.x)
    y = transformation(board_size.y)
    return Tiles(x, y)


def _in_board(board_size, pos):
    in_h = 0 <= pos.x < board_size.x
    in_v = 0 <= pos.y < board_size.y
    return in_h and in_v


def _in_snake(snake):
    return _snake_head(snake) in _snake_body(snake)


def _initial_snake(board_size):
    return [_board_pos(board_size, _center)]


def _move(pos, direction):
    x = pos.x + direction.x
    y = pos.y + direction.y
    return Tiles(x, y)


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
    return -direction.x, -direction.y


def _new_food(board_size, snake):
    while True:
        food = _board_pos(board_size, _random)
        if food not in snake:
            return food


def initial_state(board_size):
    snake = _initial_snake(board_size)
    food = _new_food(board_size, snake)
    return State(snake, food, _initial_direction, _initial_direction)


def _turn(direction, state):
    snake_has_body = _snake_has_body(state.snake)
    goes_backwards = direction == _opposite_direction(state.current_direction)

    void_movement = snake_has_body and goes_backwards
    if void_movement:
        return state
    else:
        return turn(state, direction)


def _turn_func(direction):
    def turn(state):
        return _turn(direction, state)
    return turn


def _tick(board_size, state):
    snake = _extend_snake(state.snake, state.planned_direction)
    if _snake_head(snake) == state.food:
        food = _new_food(board_size, snake)
    else:
        food = state.food
        snake = _contract_snake(snake)
    _check_collision(board_size, snake)

    return tick(state, snake, food)


class Events(Enum):
    turn_up = _turn_func(Tiles(0, 1))
    turn_down = _turn_func(Tiles(0, -1))
    turn_left = _turn_func(Tiles(-1, 0))
    turn_right = _turn_func(Tiles(1, 0))
    tick = _tick
