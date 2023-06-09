import argparse

from consts import Point
from game_display import GameDisplay
from game_utils import get_random_apple_data, get_random_wall_data, size
from snake import Snake
from wall import Wall

SNAKE_COLOR = 'black'
APPLE_COLOR = 'green'
WALL_COLOR = 'blue'

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
        self.__round_num = 0
        self.__debug: bool = args.debug
        self.__max_apples: int = args.apples
        self.__max_walls: int = args.walls
        self.__gd.show_score(self.__score)

        # game's objects
        # the snake starts in the middle of the screen
        self.__snake = Snake(size.width // 2, size.height // 2, debug=args.debug)
        self.__apples: list[Point] = []
        self.__walls: list[Wall] = []

    # ------------------------------------------------------------------
    # private methods
    # ------------------------------------------------------------------

    @staticmethod
    def __check_inbounds(pos: Point) -> bool:
        def check_inbounds_helper(num: int, length: int) -> bool:
            return 0 <= num < length
        x, y = pos
        width, height = size.width, size.height
        return check_inbounds_helper(x, width) and check_inbounds_helper(y, height)

    def __get_wall_coordinates(self, wall: Wall) -> list[Point]:
        return [pos for pos in wall if self.__check_inbounds(pos)]

    def __flatten_walls(self) -> list[Point]:
        return [
            cell for wall in self.__walls
            for cell in self.__get_wall_coordinates(wall)
        ]

    def __get_occupied_cells(self) -> list[Point]:
        return self.__snake + self.__apples + self.__flatten_walls()

    def __add_walls(self):
        if len(self.__walls) < self.__max_walls:
            data = get_random_wall_data()
            wall = Wall(*data)
            occupied_cells = self.__get_occupied_cells()
            # if nothing intersects, add the wall
            if not set(wall) & set(occupied_cells):
                self.__walls.append(wall)

    def __add_apples(self):
        if len(self.__apples) < self.__max_apples:
            pos = get_random_apple_data()
            if pos not in self.__get_occupied_cells():
                self.__apples.append(pos)

    def __moves_objects(self):
        # move the snake
        not self.__debug and self.__snake.move()

        # move the walls
        if not self.__round_num % 2:
            for wall in self.__walls:
                wall.move()

        # filter out walls which are fully outside the board
        self.__walls = list(filter(self.__get_wall_coordinates, self.__walls))

    def __eat_apples(self):
        # if the snake had eaten an apple
        if not self.__debug and self.__snake.eat(self.__apples):
            self.__score += self.__snake.grow()
            self.__gd.show_score(self.__score)

        # if a wall had run over an apple
        for wall in self.__walls:
            wall.eat(self.__apples)

    def __check_collision(self):
        head = self.__snake[0]
        # if the snake had collided with anything
        if not self.__check_inbounds(head) or head in self.__snake[1:] or head in self.__flatten_walls():
            self.__snake.coordinates.pop(0)
            self.__snake.collided = True

    def __cut_snake(self):
        for wall in self.__walls:
            if wall[0] in self.__snake:
                self.__snake.cut(wall[0])

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
        not self.__debug and self.__cut_snake()
        self.__moves_objects()
        self.__eat_apples()
        not self.__debug and self.__check_collision()

    def add_objects(self):
        self.__add_walls()
        self.__add_apples()

    def draw_board(self):
        self.__draw_objects(self.__apples, APPLE_COLOR)  # drawing the apples
        self.__draw_objects(self.__snake.coordinates, SNAKE_COLOR)  # drawing the snake (unless its debug mode)
        self.__draw_objects(self.__flatten_walls(), WALL_COLOR)  # drawing the walls

    def end_round(self):
        self.__gd.end_round()  # responsible for updating the game screen
        self.__round_num += 1

    def is_over(self) -> bool:
        rounds_over = self.__round_num == self.__rounds + 1
        return rounds_over or self.__snake.collided

    def game_over(self):
        self.__gd.show_score(f'{self.__score}. Game Over!')