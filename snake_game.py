import argparse

from consts import *
from game_display import GameDisplay
from game_utils import get_random_apple_data, get_random_wall_data
from wall import Wall, get_next_pos

def check_inbounds_helper(num: int, length: int) -> bool:
    return 0 <= num < length

# noinspection PyProtectedMember
class SnakeGame:
    # ------------------------------------------------------------------
    # init methods
    # ------------------------------------------------------------------

    def __init__(self, gd: GameDisplay, args: argparse.Namespace):
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
        self.__walls: list[Wall] = []

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

    def __check_inbounds(self, pos: Point) -> bool:
        x, y = pos
        width, height = self.__gd.width, self.__gd.height
        return check_inbounds_helper(x, width) and check_inbounds_helper(y, height)

    def __get_wall_coordinates(self, wall: Wall):
        return [
            pos for pos in wall.coordinates()
            if self.__check_inbounds(pos)
        ]

    def __add_walls(self):
        if len(self.__walls) < self.__max_walls:
            wall = Wall(*get_random_wall_data())
            occupied_cells = self.__snake + self.__apples
            # if nothing intersects, add the wall
            if not set(occupied_cells) & set(wall.coordinates()):
                self.__walls.append(wall)

    # TODO check collision with walls
    def __add_apples(self):
        if len(self.__apples) < self.__max_apples:
            pos = get_random_apple_data()
            occupied_cells = self.__snake + self.__apples + [
                cell for wall in self.__walls for cell in wall.coordinates()
            ]

            if pos not in occupied_cells:
                self.__apples.append(pos)

    # TODO: add collision detection for walls
    def __move_snake(self, pos: Point):
        # check if the snake has crossed itself or the boundaries
        if not self.__check_inbounds(pos) or pos in self.__snake:
            self.__out_of_bounds = True
        else:
            self.__snake.insert(0, pos)  # add the new position as the snake's head

        # the snake will grow as long as grow_counter is bigger than 0
        if self.__grow_counter <= 0 or self.__out_of_bounds:
            self.__snake.pop()

    def __eat_apple(self):
        self.__update_score(int(len(self.__snake) ** 0.5))
        self.__grow_counter += GROW_BONUS + int(not self.__grow_counter)
        self.__apples.remove(self.__snake[0])

    def __update_score(self, score: int):
        self.__score += score
        self.__gd.show_score(self.__score)

    def __move_wall(self, wall: Wall):
        wall.move()
        head = wall.coordinates()[0]
        if head in self.__apples:
            self.__apples.remove(head)
        # if the wall is fully out of bounds
        if not self.__get_wall_coordinates(wall):
            self.__walls.remove(wall)

    def __draw_objects(self, cells: list[Point], color: str):
        for x, y in cells:
            self.__gd.draw_cell(x, y, color)

    # ------------------------------------------------------------------
    # public methods
    # ------------------------------------------------------------------

    def read_key(self):
        key_clicked = self.__gd.get_key_clicked()
        # if we input a direction which is not the inverse to our current one
        if key_clicked and key_clicked != inverse_directions[self.__facing]:
            self.__facing = key_clicked

    # TODO: support walls
    def update_objects(self):
        # move walls every even round
        if not self.__gd._round_num % 2:
            for wall in self.__walls:
                self.__move_wall(wall)

        # activate the snake-related functions (as long as it's not debug mode)
        if not self.__debug:
            pos = get_next_pos(self.__snake[0], self.__facing)
            self.__move_snake(pos)
            if self.__snake[0] in self.__apples:
                self.__eat_apple()

    def add_objects(self):
        self.__add_walls()
        self.__add_apples()

    def draw_board(self):
        self.__draw_objects(self.__apples, APPLE_COLOR)  # drawing the apples
        not self.__debug and self.__draw_objects(self.__snake, SNAKE_COLOR)  # drawing the snake (unless its debug mode)
        for wall in self.__walls:  # lastly, drawing the walls
            self.__draw_objects(self.__get_wall_coordinates(wall), WALL_COLOR)

    def end_round(self):
        self.__gd.end_round()  # responsible for updating the game screen
        if self.__grow_counter > 0:  # ticking down the counter at the end of each round
            self.__grow_counter -= 1

    def is_over(self) -> bool:
        rounds_over = self.__gd._round_num == self.__rounds
        return rounds_over or self.__out_of_bounds

    def game_over(self):
        self.__gd.show_score(f'{self.__score}. Game Over!')