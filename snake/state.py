__all__ = ["State"]


class State:
    def __init__(self, board_size, snake, direction, food):
        self.board_size = board_size
        self.snake = snake
        self.direction = direction
        self.food = food
