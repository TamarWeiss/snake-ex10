import time

from game_display import GameDisplay

SNAKE_SIZE = 3
SNAKE_COLOR = 'black'

class SnakeGame:
    def __init__(self, gd: GameDisplay, rounds: int) -> None:
        self.__key_clicked = None
        self.__gd = gd
        self.__rounds = rounds
        self.__out_of_bounds = False

        # rudimentary snake variable
        self.__snake: list[tuple[int, int]] = [(self.__gd.width // 2, self.__gd.height // 2)]
        for i in range(1, SNAKE_SIZE):
            x, y = self.__snake[-1]
            if y - 1 < 0: break;  # if the snake is too large, break
            self.__snake.append((x, y - 1))

        gd.show_score(0)

    def read_key(self) -> None:
        self.__key_clicked = self.__gd.get_key_clicked()

    @staticmethod
    def __check_bounds(num: int, length: int):
        return 0 <= num < length

    # TODO: add collision detection for walls
    def __move_snake(self, x: int, y: int, grow=False):
        # if the snake hasn't touched itself or the boundaries
        if not self.__check_bounds(x, self.__gd.width) or not self.__check_bounds(y, self.__gd.width)\
                or (x, y) in self.__snake[1:]:
            self.__out_of_bounds = True
            self.__snake = self.__snake[:1]
            return

        if (x, y) != self.__snake[0]:  # while the head moves
            self.__snake.insert(0, (x, y))  # add to new location as the snake's add
            not grow and self.__snake.pop()  # remove the last cell of the snake (unless said otherwise)

    # TODO: support other objects
    def update_objects(self) -> None:
        x, y = self.__snake[0]
        key_clicked = self.__key_clicked
        if key_clicked == 'Left':
            x -= 1
        elif key_clicked == 'Right':
            x += 1
        elif key_clicked == 'Down':
            y -= 1
        elif key_clicked == 'Up':
            y += 1

        self.__move_snake(x, y)

    # TODO: support other objects
    def draw_board(self) -> None:
        for x, y in self.__snake:  # draws the snake.
            self.__gd.draw_cell(x, y, SNAKE_COLOR)

    # TODO: what does this handle?
    def end_round(self) -> None:
        self.__gd.end_round()  # responsible for updating the game screen

    def is_over(self) -> bool:
        # noinspection PyProtectedMember
        rounds_over = self.__gd._round_num == self.__rounds
        return rounds_over or self.__out_of_bounds

    def game_over(self):
        self.__gd.show_score('Game Over!')
        time.sleep(2)