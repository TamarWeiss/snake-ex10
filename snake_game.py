import argparse

import game_utils
from consts import *
from game_display import GameDisplay

def check_inbounds(num: int, length: int) -> bool:
    return 0 <= num < length

def get_next_pos(head: Point, direction: str) -> Point:
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

        self.__snake = self.__init_snake()
        self.__apples: list[Point] = []
        self.__walls: list[list[Point]] = []

        self.__add_apples()

    def __init_snake(self) -> list[Point]:
        if not self.__debug:
            x, y = self.__gd.width // 2, self.__gd.height // 2  # the snake starts in the middle of the screen
            return [
                (x, y - i)
                for i in range(SNAKE_SIZE)
                if y - i >= 0
            ]
        return []

    # ------------------------------------------------------------------
    # private methods
    # ------------------------------------------------------------------

    # TODO check collision with walls
    def __add_apples(self):
        if len(self.__apples) < self.__max_apples:
            pos = game_utils.get_random_apple_data()
            occupied_cells = self.__snake + self.__apples
            if pos not in occupied_cells:
                self.__apples.append(pos)

    # TODO: add collision detection for walls
    def __move_snake(self, pos: Point) -> None:
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

    def __eat_apple(self) -> None:
        self.__update_score(int(len(self.__snake) ** 0.5))
        self.__grow_counter += GROW_BONUS + int(not self.__grow_counter)
        self.__apples.remove(self.__snake[0])

    def __update_score(self, score: int) -> None:
        self.__score += score
        self.__gd.show_score(self.__score)

    def __draw_objects(self, cells: list[Point], color: str) -> None:
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

    # TODO: support walls
    def update_objects(self) -> None:
        # move walls before snake
        if not self.__debug:  # activate the snake-related functions (as long as it's not debug mode)
            pos = get_next_pos(self.__snake[0], self.__facing)
            self.__move_snake(pos)
            if self.__snake[0] in self.__apples:
                self.__eat_apple()

    def add_objects(self):
        # add walls before
        self.__add_apples()

    def draw_board(self) -> None:
        self.__draw_objects(self.__apples, APPLE_COLOR)  # drawing the apples
        not self.__debug and self.__draw_objects(self.__snake, SNAKE_COLOR)  # drawing the snake (unless its debug mode)
        for wall in self.__walls:  # lastly, drawing the walls
            self.__draw_objects(wall, WALL_COLOR)

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