from consts import Point
from movable import Movable

class Wall(Movable):
    def __init__(self, x: int, y: int, direction: str):
        super().__init__(direction)
        self.coordinates = self.__set_coordinates((x, y))

    def __set_coordinates(self, center) -> list[Point]:
        prev_point = self.get_next_pos(center)
        next_point = self.get_next_pos(center, inverse=True)
        return [next_point, center, prev_point]