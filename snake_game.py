from game_display import GameDisplay

SNAKE_SIZE = 3
SNAKE_COLOR = 'black'
LEFT = 'Left'
RIGHT = 'Right'
DOWN = 'Down'
UP = 'Up'

# a dictionary which maps an inverse direction to each direction
inverse_directions = {
    LEFT: RIGHT,
    RIGHT: LEFT,
    DOWN: UP,
    UP: DOWN
}

class SnakeGame:
    def __init__(self, gd: GameDisplay, rounds: int) -> None:
        self.__key_clicked = None
        self.__gd = gd
        self.__rounds = rounds
        self.__out_of_bounds = False
        self.__facing = UP
        self.__update_score(0)

        # rudimentary snake variable
        self.__snake: list[tuple[int, int]] = [(self.__gd.width // 2, self.__gd.height // 2)]
        for i in range(1, SNAKE_SIZE):
            x, y = self.__snake[-1]
            if y - 1 < 0: break;  # if the snake is too large for the screen, break
            self.__snake.append((x, y - 1))

    def read_key(self) -> None:
        key_clicked = self.__gd.get_key_clicked()
        # if we input a direction which not the inverse to our current one
        if key_clicked and key_clicked != inverse_directions[self.__facing]:
            self.__facing = key_clicked

    @staticmethod
    def __check_inbounds(num: int, length: int):
        return 0 <= num < length

    # TODO: add collision detection for walls
    def __move_snake(self, x: int, y: int, grow=False):
        is_OOB = not self.__check_inbounds(x, self.__gd.width) or not self.__check_inbounds(y, self.__gd.height)
        # check if the snake has crossed itself or the screen boundaries
        if is_OOB or (x, y) in self.__snake:
            self.__out_of_bounds = True
            self.__snake = self.__snake[:1]
        else:
            self.__snake.insert(0, (x, y))  # add the new position as the snake's head
            not grow and self.__snake.pop()  # remove the last cell of the snake (unless said otherwise)

    # TODO: support other objects
    def update_objects(self) -> None:
        x, y = self.__snake[0]
        facing = self.__facing

        if facing == LEFT:
            x -= 1
        elif facing == RIGHT:
            x += 1
        elif facing == DOWN:
            y -= 1
        elif facing == UP:
            y += 1

        self.__move_snake(x, y)

    # TODO: flag snake to grow after this. currently unused
    def __eat_apple(self):
        self.__update_score(int(len(self.__snake) ** 0.5))

    def __update_score(self, score):
        self.__score = score
        self.__gd.show_score(self.__score)

    # TODO: support other objects
    def draw_board(self) -> None:
        for x, y in self.__snake:  # draws the snake.
            self.__gd.draw_cell(x, y, SNAKE_COLOR)

    # TODO: what does this handle beside gd?
    def end_round(self) -> None:
        self.__gd.end_round()  # responsible for updating the game screen

    def is_over(self) -> bool:
        # noinspection PyProtectedMember
        rounds_over = self.__gd._round_num == self.__rounds
        return rounds_over or self.__out_of_bounds

    def game_over(self):
        self.__update_score(f'Game Over! Final score: {self.__score}')