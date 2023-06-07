from consts import GROW_BONUS, Point, SNAKE_SIZE, UP
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

    def get_next_pos(self, pos=None, inverse=False) -> Point:
        return super().get_next_pos(pos or self[0], inverse)

    def move(self):
        pos = self.get_next_pos()
        # check if the snake has crossed itself
        if pos in self.coordinates:
            self.flag_collision()
        elif not self.collided:  # if it hadn't collided with somthing already
            self.coordinates.insert(0, pos)  # add the new position as the snake's head

        # the snake will grow as long as grow_counter is bigger than 0
        if not self.__grow_counter:
            self.coordinates.pop()
        self.__count_down()

    def eat(self, apples: list[Point]):
        apples.remove(self[0])
        self.__grow_counter += GROW_BONUS
        return int(len(self) ** 0.5)

    def flag_collision(self):
        self.collided = True