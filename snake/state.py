__all__ = ["State"]


class State:
    def __init__(self, snake, direction, food):
        self.snake = snake
        self.food = food

        self.current_direction = direction
        self.planned_direction = direction
