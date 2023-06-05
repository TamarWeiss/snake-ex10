import time

from game_display import GameDisplay

SNAKE_SIZE = 3
SNAKE_COLOR = 'black'

class SnakeGame:
    def __init__(self, gd: GameDisplay, rounds: int) -> None:
        self.__key_clicked = None
        self.__gd = gd
        self.__rounds = rounds

        # rudimentary snake variable
        self.__snake: list[tuple[int, int]] = [(self.__gd.width // 2, self.__gd.height // 2)]
        for i in range(1, SNAKE_SIZE):
            x, y = self.__snake[-1]
            if y - 1 < 0: break;  # if the snake is too large, break
            self.__snake.append((x, y - 1))

        gd.show_score(0)

    def read_key(self) -> None:
        self.__key_clicked = self.__gd.get_key_clicked()

    def __move_snake(self, x: int, y: int, grow=False):
        if (x, y) != self.__snake[0]:  # while the head moves
            self.__snake.insert(0, (x, y))  # add to new location as the snake's add
            not grow and self.__snake.pop()  # remove the last cell of the snake (unless said otherwise)

    # TODO: support other objects?
    def update_objects(self) -> None:
        x, y = self.__snake[0]
        key_clicked = self.__key_clicked
        if (key_clicked == 'Left') and (x > 0):
            x -= 1
        elif (key_clicked == 'Right') and (x < self.__gd.width - 1):
            x += 1
        elif (key_clicked == 'Down') and (y > 0):
            y -= 1
        elif (key_clicked == 'Up') and (y < self.__gd.height - 1):
            y += 1
        self.__move_snake(x, y)

    # TODO: support other objects?
    def draw_board(self) -> None:
        for x, y in self.__snake:  # draws the snake.
            self.__gd.draw_cell(x, y, SNAKE_COLOR)

    # TODO: what does this handle?
    def end_round(self) -> None:
        self.__gd.end_round()

    # TODO: how we determine when snake is out-of-bounds, or when the round num reached its limit?
    def is_over(self) -> bool:
        # noinspection PyProtectedMember
        return self.__gd._round_num == self.__rounds

    def game_over(self):
        self.__gd.show_score('Game Over!')
        time.sleep(2)