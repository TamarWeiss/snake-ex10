from typing import Optional

from consts import GROW_BONUS, SNAKE_SIZE, UP, inverse_directions
from wall import get_next_pos

class Snake:
    def __init__(self, x: int, y: int):
        self.__facing = UP
        self.__grow_counter = 0
        self.collided = False
        self.coordinates = [
            (x, y - i)
            for i in range(SNAKE_SIZE)
            if y - i >= 0
        ]

    def __count_down(self):
        if self.__grow_counter > 0:  # ticking down the counter one at a time
            self.__grow_counter -= 1

    def turn(self, direction: Optional[str]):
        # if the direction is not the inverse to our current one
        if direction and direction != inverse_directions[self.__facing]:
            self.__facing = direction

    def move(self):
        coordinates = self.coordinates
        pos = get_next_pos(coordinates[0], self.__facing)
        # check if the snake has crossed itself or the boundaries
        if pos in self.coordinates:
            self.flag_collision()
        else:
            coordinates.insert(0, pos)  # add the new position as the snake's head

        # the snake will grow as long as grow_counter is bigger than 0
        self.__count_down()

    def grow(self):
        self.__grow_counter += GROW_BONUS + int(not self.__grow_counter)

    def flag_collision(self):
        self.collided = True