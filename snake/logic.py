from collections import namedtuple
from math import floor
from random import randint


__all__ = ["BoardSize", "Events", "State"]


_INITIAL_DIRECTION = (1, 0)


class _Collision(RuntimeError):
    pass


class _CollisionWithWall(_Collision):
    pass


class _CollisionWithSnake(_Collision):
    pass


def _random(num_tiles):
    return randint(0, num_tiles - 1)


def _center(num_tiles):
    return floor(num_tiles / 2)


def _board_pos(board_size, transformation):
    x = transformation(board_size.x)
    y = transformation(board_size.y)
    return _BoardPos(x, y)


def _in_board(board_size, pos):
    in_h = 0 <= pos.x < board_size.x
    in_v = 0 <= pos.y < board_size.y
    return in_h and in_v


def _check_collision(board_size, snake):
    if not _in_board(board_size, snake.head):
        raise _CollisionWithWall
    if snake.head in snake.body:
        raise _CollisionWithSnake


def _new_food(board_size, snake):
    while True:
        food = _board_pos(board_size, _random)
        if food not in snake:
            return food


class _Tiles(namedtuple("_Tiles", ("x", "y"))):
    pass


class _BoardPos(_Tiles):
    def move(self, direction):
        x = self.x + direction.x
        y = self.y + direction.y
        cls = type(self)
        return cls(x, y)


class _Direction(namedtuple("_Direction", ("x", "y"))):
    @classmethod
    def initial(cls):
        return cls(*_INITIAL_DIRECTION)

    def opposite(self):
        cls = type(self)
        return cls(-self.x, -self.y)


class _Snake:
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
        new_head = self.head.move(direction)
        cls = type(self)
        return cls([new_head] + self.pos)

    def contract(self):
        cls = type(self)
        return cls(self.pos[:-1])


class _Tick(namedtuple("_Tick", ("board_size",))):
    def __call__(self, state):
        snake = state.snake.extend(state.planned_direction)
        if snake.head == state.food:
            food = _new_food(self.board_size, snake)
        else:
            food = state.food
            snake = snake.contract()
        _check_collision(self.board_size, snake)

        return state.tick(snake, food)


class _Turn(namedtuple("_Turn", ("direction",))):

    def __call__(self, state):
        goes_backwards = self.direction == state.current_direction.opposite()

        void_movement = state.snake.body and goes_backwards
        if void_movement:
            return state
        else:
            return state.turn(self.direction)


class BoardSize(_Tiles):
    pass


class State(
    namedtuple("State", ("snake", "food", "current_direction", "planned_direction"))
):
    @classmethod
    def initial(cls, board_size):
        snake = _Snake.initial(board_size)
        food = _new_food(board_size, snake)
        direction = _Direction.initial()
        return cls(snake, food, direction, direction)

    def tick(self, snake, food):
        cls = type(self)
        return cls(snake, food, self.planned_direction, self.planned_direction)

    def turn(self, direction):
        cls = type(self)
        return cls(self.snake, self.food, self.current_direction, direction)


class Events:
    def __init__(self, board_size):
        self.board_size = board_size
        self.turn_up = _Turn(_Direction(0, 1))
        self.turn_down = _Turn(_Direction(0, -1))
        self.turn_left = _Turn(_Direction(-1, 0))
        self.turn_right = _Turn(_Direction(1, 0))
        self.tick = _Tick(board_size)
