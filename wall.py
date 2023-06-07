from consts import Point
from movable import Movable

class Wall(Movable):
    def __init__(self, x: int, y: int, direction: str):
        super().__init__(direction)
        self.coordinates = self.__get_coordinates((x, y))

    def __get_center(self) -> Point:
        return self.coordinates[len(self) // 2]

    def __get_coordinates(self, center) -> list[Point]:
        prev_point = self.get_next_pos(center)
        next_point = self.get_next_pos(center, inverse=True)
        return [next_point, center, prev_point]

    def move(self, apples: list[Point]):
        pos = self.get_next_pos(self.__get_center())
        self.coordinates = self.__get_coordinates(pos)
        if self[0] in apples:
            apples.remove(self[0])