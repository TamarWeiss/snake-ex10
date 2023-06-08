from typing import Generator, Optional, Sequence

from consts import DOWN, LEFT, Point, RIGHT, UP, inverse_directions

class Movable(Sequence):
    def __init__(self, direction: str):
        self.__direction = direction
        self.coordinates: list[Point] = []

    def get_next_pos(self, pos: Point = None, inverse=False) -> Point:
        x, y = pos or self[0]
        direction = self.__direction if not inverse else inverse_directions[self.__direction]
        x += -int(direction == LEFT) + int(direction == RIGHT)
        y += -int(direction == DOWN) + int(direction == UP)
        return x, y

    def turn(self, direction: Optional[str]):
        # if the direction is not the inverse to our current one
        if direction and direction != inverse_directions[self.__direction]:
            self.__direction = direction

    def move(self, collided=False, grow=False):
        pos = self.get_next_pos()
        not collided and self.coordinates.insert(0, pos)
        not grow and self.coordinates.pop()

    def eat(self, apples: list[Point]) -> bool:
        if self[0] in apples:
            apples.remove(self[0])
            return True
        return False

    def __len__(self) -> int:
        return len(self.coordinates)

    def __getitem__(self, index: int) -> Point:
        return self.coordinates[index]

    def __iter__(self) -> Generator[Point, ..., ...]:
        return (cell for cell in self.coordinates)

    def __contains__(self, item: Point) -> bool:
        return item in self.coordinates

    def __add__(self, other: list[Point]) -> list[Point]:
        return self.coordinates + other