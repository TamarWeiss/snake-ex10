from consts import Point, UP
from movable import Movable

SNAKE_SIZE = 3
GROW_BONUS = 3

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

    def move(self, grow=False):
        super().move(self.__grow_counter)
        self.__count_down()

    def grow(self) -> int:
        self.__grow_counter += GROW_BONUS
        return int(len(self) ** 0.5)

    def cut(self, point: Point):
        index = self.coordinates.index(point)
        self.coordinates = self[:index]
        if len(self) <= 1:
            self.collided = True