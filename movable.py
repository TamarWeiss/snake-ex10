from typing import Optional, Sequence, overload

from consts import *

class Movable(Sequence):
    def __init__(self, direction: str):
        self.__direction = direction
        self.coordinates: list[Point] = []

    def get_next_pos(self, pos: Point = None, inverse=False) -> Point:
        x, y = pos or self[0]
        direction = self.__direction if not inverse else inverse_directions.get(self.__direction)
        x += -int(direction == LEFT) + int(direction == RIGHT)
        y += -int(direction == DOWN) + int(direction == UP)
        return x, y

    def turn(self, direction: Optional[str]):
        # if the direction is not the inverse to our current one
        if direction and direction != inverse_directions.get(self.__direction):
            self.__direction = direction

    def move(self, grow=False):
        pos = self.get_next_pos()
        if pos != self[0]:  # check if it really moved
            self.coordinates.insert(0, pos)
            not grow and self.coordinates.pop()

    def eat(self, apples: list[Point]) -> bool:
        if self[0] in apples:
            apples.remove(self[0])
            return True
        return False

    def __len__(self) -> int:
        return len(self.coordinates)

    @overload
    def __getitem__(self, index: int) -> Point:
        return self.coordinates[index]

    def __getitem__(self, index: slice) -> list[Point]:
        return self.coordinates[index]

    def __add__(self, other: list[Point]) -> list[Point]:
        return self.coordinates + other