from collections import namedtuple

__all__ = ["State", "tick"]


State = namedtuple("State", ("snake", "food", "current_direction", "planned_direction"))


def tick(state, snake, food):
    return State(snake, food, state.planned_direction, state.planned_direction)


def turn(state, direction):
    return State(state.snake, state.food, state.current_direction, direction)
