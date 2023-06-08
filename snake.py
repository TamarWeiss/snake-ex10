from typing import Optional

from consts import GROW_BONUS, SNAKE_SIZE, UP, inverse_directions
from movable import Movable

class Snake(Movable):
    def __init__(self, x: int, y: int, debug=False):
        super().__init__(UP)
        self.__grow_counter = 0
        self.collided = False
        if not debug:
            self.coordinates = [
                (x, y - i)
                for i in range(SNAKE_SIZE)
                if y - i >= 0
            ]

    def __count_down(self):
        # ticking down the counter one at a time
        if self.__grow_counter > 0:
            self.__grow_counter -= 1

    def turn(self, direction: Optional[str]):
        # if the direction is not the inverse to our current one
        if direction and direction != inverse_directions[self.__direction]:
            self.__direction = direction

    def move(self, collided=False, grow=False):
        self.collided = collided
        super().move(self.collided, bool(self.__grow_counter))
        self.__count_down()

    def grow(self) -> int:
        self.__grow_counter += GROW_BONUS
        return int(len(self) ** 0.5)