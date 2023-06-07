from typing import Optional

from consts import GROW_BONUS, Point, SNAKE_SIZE, UP, inverse_directions
from wall import get_next_pos

class Snake:
    def __init__(self, x: int, y: int, debug=False):
        self.__facing = UP
        self.__grow_counter = 0
        self.collided = False
        self.coordinates = [
            (x, y - i)
            for i in range(SNAKE_SIZE)
            if y - i >= 0
        ] if not debug else []

    def __count_down(self):
        # ticking down the counter one at a time
        if self.__grow_counter > 0:
            self.__grow_counter -= 1

    def turn(self, direction: Optional[str]):
        # if the direction is not the inverse to our current one
        if direction and direction != inverse_directions[self.__facing]:
            self.__facing = direction

    def get_next_pos(self) -> Point:
        return get_next_pos(self[0], self.__facing)

    def move(self, pos: Point):
        # check if the snake has crossed itself
        if pos in self.coordinates:
            self.flag_collision()
        elif not self.collided:  # if it hasn't collided with somthing already
            self.coordinates.insert(0, pos)  # add the new position as the snake's head

        # the snake will grow as long as grow_counter is bigger than 0
        if not self.__grow_counter or self.collided:
            self.coordinates.pop()
        self.__count_down()

    def grow(self):
        self.__grow_counter += GROW_BONUS
        return int(len(self) ** 0.5)

    def flag_collision(self):
        self.collided = True

    def __len__(self) -> int:
        return len(self.coordinates)

    def __getitem__(self, index: int) -> Point:
        return self.coordinates[index]

    def __add__(self, other: list[Point]) -> list[Point]:
        return self.coordinates + other