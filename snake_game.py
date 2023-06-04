from typing import Optional

from game_display import GameDisplay
from game_utils import size

SNAKE_SIZE = 3
COLOR = 'black'

class SnakeGame:
    def __init__(self) -> None:
        self.__x = size.width // 2
        self.__y = size.height // 2
        self.__key_clicked = None
        self.__width = size.width
        self.__height = size.height

        # rudimentary snake variable
        self.__snake: list[tuple[int, int]] = [(size.width // 2, size.height // 2)]
        for i in range(1, SNAKE_SIZE):
            x, y = self.__snake[-1]
            if y - 1 < 0: break;  # if the snake is too large, break
            self.__snake.append((x, y - 1))

    def read_key(self, key_clicked: Optional[str]) -> None:
        self.__key_clicked = key_clicked

    def __move_snake(self, grow=False):
        if (self.__x, self.__y) not in self.__snake:
            self.__snake.insert(0, (self.__x, self.__y))  # add to new location as the snake's add
            not grow and self.__snake.pop()  # remove the last cell of the snake (unless said otherwise)

    # TODO: support other objects?
    def update_objects(self) -> None:
        if (self.__key_clicked == 'Left') and (self.__x > 0):
            self.__x -= 1
        elif (self.__key_clicked == 'Right') and (self.__x < self.__width - 1):
            self.__x += 1
        if (self.__key_clicked == 'Down') and (self.__y > 0):
            self.__y -= 1
        elif (self.__key_clicked == 'Up') and (self.__y < self.__height - 1):
            self.__y += 1
        self.__move_snake()

    # TODO: support other objects?
    def draw_board(self, gd: GameDisplay) -> None:
        for x, y in self.__snake:  # draws the snake.
            gd.draw_cell(x, y, COLOR)

    # TODO: what does this handle?
    def end_round(self) -> None:
        pass

    # TODO: how we determine when snake is out-of-bounds, or when the round num reached its limit?
    # How do we access round_num of GameDisplay?
    def is_over(self) -> bool:
        return False