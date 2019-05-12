from collections import namedtuple
from enum import Enum
from math import floor
from random import randint
from snake.state import State


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


def _move(pos, direction):
    x = pos.x + direction.x
    y = pos.y + direction.y
    return Tiles(x, y)


def _check_collision(board_size, snake):
    if not _in_board(board_size, snake.head):
        raise CollisionWithWall
    if snake.head in snake.body:
        raise CollisionWithSnake


def _opposite_direction(direction):
    return -direction.x, -direction.y


def _new_food(board_size, snake):
    while True:
        food = _board_pos(board_size, _random)
        if food not in snake:
            return food


def initial_state(board_size):
    snake = Snake.initial(board_size)
    food = _new_food(board_size, snake)
    return State(snake, food, _initial_direction, _initial_direction)


class Snake:
    @classmethod
    def initial(cls, board_size):
        initial_pos = _board_pos(board_size, _center)
        return cls([initial_pos])

    def __init__(self, pos):
        self.pos = pos

    def __contains__(self, pos):
        return pos in self.pos

    def __len__(self):
        return len(self.pos)

    def __getitem__(self, key):
        return self.pos[key]

    @property
    def head(self):
        return self.pos[0]

    @property
    def body(self):
        return self.pos[1:]

    def extend(self, direction):
        new_head = _move(self.head, direction)
        return Snake([new_head] + self.pos)

    def contract(self):
        return Snake(self.pos[:-1])


class Tick:
    def __init__(self, board_size):
        self.board_size = board_size

    def __call__(self, state):
        snake = state.snake.extend(state.planned_direction)
        if snake.head == state.food:
            food = _new_food(self.board_size, snake)
        else:
            food = state.food
            snake = snake.contract()
        _check_collision(self.board_size, snake)

        return state.tick(snake, food)


class Turn:

    def __init__(self, direction):
        self.direction = direction

    def __call__(self, state):
        goes_backwards = self.direction == _opposite_direction(state.current_direction)

        void_movement = state.snake.body and goes_backwards
        if void_movement:
            return state
        else:
            return state.turn(self.direction)


class Events:
    def __init__(self, board_size):
        self.board_size = board_size
        self.turn_up = Turn(Tiles(0, 1))
        self.turn_down = Turn(Tiles(0, -1))
        self.turn_left = Turn(Tiles(-1, 0))
        self.turn_right = Turn(Tiles(1, 0))
        self.tick = Tick(board_size)
