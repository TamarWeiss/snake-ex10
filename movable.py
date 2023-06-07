from abc import abstractmethod
from typing import Optional, Sequence

from consts import DOWN, LEFT, Point, RIGHT, UP, inverse_directions

class Movable(Sequence):
    def __init__(self, direction: str):
        self.__direction = direction
        self.coordinates: list[Point] = []

    def turn(self, direction: Optional[str]):
        # if the direction is not the inverse to our current one
        if direction and direction != inverse_directions[self.__direction]:
            self.__direction = direction

    def get_next_pos(self, pos: Point, inverse=False) -> Point:
        x, y = pos
        direction = self.__direction if not inverse else inverse_directions[self.__direction]
        x += -int(direction == LEFT) + int(direction == RIGHT)
        y += -int(direction == DOWN) + int(direction == UP)
        return x, y

    def eat(self, apples: list[Point]) -> bool:
        if self[0] in apples:
            apples.remove(self[0])
            return True
        return False

    @abstractmethod
    def move(self):
        pass

    def __len__(self) -> int:
        return len(self.coordinates)

    def __getitem__(self, index: int) -> Point:
        return self.coordinates[index]

    def __iter__(self):
        return (cell for cell in self.coordinates)

    def __add__(self, other: list[Point]) -> list[Point]:
        return self.coordinates + other