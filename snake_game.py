import argparse

from consts import *
from game_display import GameDisplay
from game_utils import get_random_apple_data, get_random_wall_data
from snake import Snake
from wall import Wall

# noinspection PyProtectedMember
class SnakeGame:
    # ------------------------------------------------------------------
    # init method
    # ------------------------------------------------------------------

    def __init__(self, gd: GameDisplay, args: argparse.Namespace):
        self.__gd = gd
        self.__rounds: int = args.rounds
        self.__out_of_bounds = False
        self.__score = 0
        self.__debug: bool = args.debug
        self.__max_apples: int = args.apples
        self.__max_walls: int = args.walls
        self.__gd.show_score(self.__score)

        # game's objects
        # the snake starts in the middle of the screen
        self.__snake = Snake(self.__gd.width // 2, self.__gd.height // 2, args.debug)
        self.__apples: list[Point] = []
        self.__walls: list[Wall] = []

    # ------------------------------------------------------------------
    # private methods
    # ------------------------------------------------------------------

    def __check_inbounds(self, pos: Point) -> bool:
        def check_inbounds_helper(num: int, length: int) -> bool:
            return 0 <= num < length
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

    def __add_apples(self):
        if len(self.__apples) < self.__max_apples:
            pos = get_random_apple_data()
            occupied_cells = self.__snake + self.__apples + [
                cell for wall in self.__walls for cell in wall.coordinates()
            ]

            if pos not in occupied_cells:
                self.__apples.append(pos)

    # TODO: add collision detection for walls
    def __move_snake(self):
        pos = self.__snake.get_next_pos()
        # check if the snake has crossed the boundaries
        if not self.__check_inbounds(pos):
            self.__snake.flag_collision()
        self.__snake.move(pos)

    def __eat_apple(self):
        score = self.__snake.eat(self.__apples)
        self.__update_score(score)

    def __update_score(self, score: int):
        self.__score += score
        self.__gd.show_score(self.__score)

    def __move_wall(self, wall: Wall):
        wall.move(self.__apples)
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
        self.__snake.turn(key_clicked)

    def update_objects(self):
        # move walls every even round
        if not self.__gd._round_num % 2:
            for wall in self.__walls:
                self.__move_wall(wall)

        # activate the snake-related functions (as long as it's not debug mode)
        if not self.__debug:
            self.__move_snake()
            if self.__snake[0] in self.__apples:
                self.__eat_apple()

    def add_objects(self):
        self.__add_walls()
        self.__add_apples()

    def draw_board(self):
        self.__draw_objects(self.__apples, APPLE_COLOR)  # drawing the apples
        if not self.__debug:  # drawing the snake (unless its debug mode)
            self.__draw_objects(self.__snake.coordinates, SNAKE_COLOR)
        for wall in self.__walls:  # lastly, drawing the walls
            self.__draw_objects(self.__get_wall_coordinates(wall), WALL_COLOR)

    def end_round(self):
        self.__gd.end_round()  # responsible for updating the game screen

    def is_over(self) -> bool:
        rounds_over = self.__gd._round_num == self.__rounds
        return rounds_over or self.__snake.collided

    def game_over(self):
        self.__gd.show_score(f'{self.__score}. Game Over!')