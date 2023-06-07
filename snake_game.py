import argparse

from consts import *
import game_utils
from game_display import GameDisplay

Location = tuple[int, int]

def check_inbounds(num: int, length: int) -> bool:
    return 0 <= num < length

def get_next_pos(head: Location, direction: str) -> Location:
    x, y = head
    x += -int(direction == LEFT) + int(direction == RIGHT)
    y += -int(direction == DOWN) + int(direction == UP)
    return x, y

class SnakeGame:
    # ------------------------------------------------------------------
    # init methods
    # ------------------------------------------------------------------

    def __init__(self, gd: GameDisplay, args: argparse.Namespace) -> None:
        self.__gd = gd
        self.__rounds: int = args.rounds
        self.__out_of_bounds = False
        self.__facing = UP
        self.__score = 0
        self.__grow_counter = 0
        self.__debug: bool = args.debug
        self.__max_apples: int = args.apples
        self.__max_walls: int = args.walls
        self.__gd.show_score(self.__score)

        # game's objects
        if not self.__debug:
            self.__snake = self.__init_snake()
        self.__apples: list[Location] = []
        self.__walls: list[list[Location]] = []

    def __init_snake(self) -> list[Location]:
        x, y = self.__gd.width // 2, self.__gd.height // 2  # the snake starts in the middle of the screen
        return [
            (x, y - i)
            for i in range(SNAKE_SIZE)
            if y - i >= 0
        ]
    # TODO check collision with walls
    def __init_apples(self):
        """this method initializes the apples"""
        x, y = game_utils.get_random_apple_data()
        if (x, y) not in self.__snake:
            self.__apples.append((x,y))

    # TODO check collision with walls
    # TODO does this include the i + 1 round if game is over?
    def add_apples(self):
        x, y = game_utils.get_random_apple_data()
        while len(self.__apples) < self.__max_apples:
            if (x, y) not in self.__snake and (x, y) not in self.__snake and self.is_over():
                self.__apples.append((x, y))


    # ------------------------------------------------------------------
    # private methods
    # ------------------------------------------------------------------

    # TODO: add collision detection for walls
    def __move_snake(self, pos: Location) -> None:
        width, height = self.__gd.width, self.__gd.height
        is_OOB = not check_inbounds(pos[0], width) or not check_inbounds(pos[1], height)
        # check if the snake has crossed itself or the boundaries
        if is_OOB or pos in self.__snake:
            self.__out_of_bounds = True
        else:
            self.__snake.insert(0, pos)  # add the new position as the snake's head

        # the snake will grow as long as grow_counter is bigger than 0
        if self.__grow_counter <= 0 or self.__out_of_bounds:
            self.__snake.pop()

    # TODO: implement removing the apple from the list. currently unused.
    def __eat_apple(self) -> None:
        self.__update_score(int(len(self.__snake) ** 0.5))
        self.__grow_counter += GROW_BONUS
        for apple in self.__apples:
            if self.__snake[0] == apple:
                self.__apples.remove(apple)

    def __update_score(self, score: int) -> None:
        self.__score += score
        self.__gd.show_score(self.__score)

    def __draw_items(self, cells: list[Location], color: str) -> None:
        for x, y in cells:
            self.__gd.draw_cell(x, y, color)

    # ------------------------------------------------------------------
    # public methods
    # ------------------------------------------------------------------

    def read_key(self) -> None:
        key_clicked = self.__gd.get_key_clicked()
        # if we input a direction which is not the inverse to our current one
        if key_clicked and key_clicked != inverse_directions[self.__facing]:
            self.__facing = key_clicked

    # TODO: support other objects
    def update_objects(self) -> None:
        if not self.__debug:  # updates the snake object (as long as it's not debug mode)
            pos = get_next_pos(self.__snake[0], self.__facing)
            self.__move_snake(pos)

    def draw_board(self) -> None:
        self.__draw_items(self.__apples, APPLE_COLOR)  # drawing the apples
        not self.__debug and self.__draw_items(self.__snake, SNAKE_COLOR)  # drawing the snake (unless its debug mode)
        for wall in self.__walls:  # lastly, drawing the walls
            self.__draw_items(wall, WALL_COLOR)

    # TODO: grow counter should tick down at the start or at the end of each round?
    def end_round(self) -> None:
        self.__gd.end_round()  # responsible for updating the game screen
        if self.__grow_counter > 0:  # ticking down the counter at the end of each round
            self.__grow_counter -= 1

    def is_over(self) -> bool:
        # noinspection PyProtectedMember
        rounds_over = self.__gd._round_num == self.__rounds
        return rounds_over or self.__out_of_bounds

    def game_over(self) -> None:
        self.__gd.show_score(f'{self.__score}. Game Over!')