from game_display import GameDisplay

SNAKE_SIZE = 3
SNAKE_COLOR = 'black'

class SnakeGame:
    def __init__(self, gd: GameDisplay, rounds: int) -> None:
        self.__key_clicked = None
        self.__gd = gd
        self.__rounds = rounds
        self.__out_of_bounds = False
        self.__facing = 'Up'
        self.__update_score(0)

        # rudimentary snake variable
        self.__snake: list[tuple[int, int]] = [(self.__gd.width // 2, self.__gd.height // 2)]
        for i in range(1, SNAKE_SIZE):
            x, y = self.__snake[-1]
            if y - 1 < 0: break;  # if the snake is too large for the screen, break
            self.__snake.append((x, y - 1))

    def read_key(self) -> None:
        self.__key_clicked = self.__gd.get_key_clicked()

    @staticmethod
    def __check_inbounds(num: int, length: int):
        return 0 <= num < length

    # TODO: add collision detection for walls and apples
    def __move_snake(self, x: int, y: int, grow=False):
        is_OOB = not self.__check_inbounds(x, self.__gd.width) or not self.__check_inbounds(y, self.__gd.height)
        if is_OOB or (x, y) in self.__snake:  # check if the snake has crossed itself or the screen boundaries
            self.__out_of_bounds = True
            self.__snake = self.__snake[:1]
        else:
            self.__snake.insert(0, (x, y))  # add the new position as the snake's head
            not grow and self.__snake.pop()  # remove the last cell of the snake (unless said otherwise)

    # TODO: support other objects
    # TODO: revamp snake to move automatically. prevent snake from going backward.
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

        # calls __move_snake ONLY when the position is changed
        (x, y) != self.__snake[0] and self.__move_snake(x, y)

    # TODO: flag snake to grow. currently unused
    def __eat_apple(self):
        self.__update_score(int(len(self.__snake) ** 0.5))

    def __update_score(self, score: int | str):
        self.__score = score
        self.__gd.show_score(self.__score)

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
        self.__update_score(f'Game Over! Final score: {self.__score}')