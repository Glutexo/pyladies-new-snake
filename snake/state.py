from collections import namedtuple

__all__ = ["State"]


class State:
    def __init__(self, snake, food, current_direction, planned_direction):
        self.snake = snake
        self.food = food
        self.current_direction = current_direction
        self.planned_direction = planned_direction

    def tick(self, snake, food):
        return State(snake, food, self.planned_direction, self.planned_direction)

    def turn(self, direction):
        return State(self.snake, self.food, self.current_direction, direction)
