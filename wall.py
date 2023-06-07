from consts import DOWN, LEFT, Point, RIGHT, UP, inverse_directions

def get_next_pos(head: Point, direction: str) -> Point:
    x, y = head
    x += -int(direction == LEFT) + int(direction == RIGHT)
    y += -int(direction == DOWN) + int(direction == UP)
    return x, y

class Wall:
    def __init__(self, x: int, y: int, direction: str):
        self.__center = (x, y)
        self.__direction = direction

    def coordinates(self) -> list[Point]:
        center = self.__center
        direction = self.__direction
        prev_point = get_next_pos(center, direction)
        next_point = get_next_pos(center, inverse_directions[direction])
        return [next_point, center, prev_point]

    def move(self):
        self.__center = get_next_pos(self.__center, self.__direction)