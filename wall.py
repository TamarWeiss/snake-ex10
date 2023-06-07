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

    def __coordinates(self) -> list[Point]:
        center = self.__center
        direction = self.__direction
        prev_point = get_next_pos(center, direction)
        next_point = get_next_pos(center, inverse_directions[direction])
        return [next_point, center, prev_point]

    def move(self, apples: list[Point]):
        self.__center = get_next_pos(self.__center, self.__direction)
        head = self[0]
        if head in apples:
            apples.remove(head)

    def __getitem__(self, index: int) -> Point:
        return self.__coordinates()[index]

    def __iter__(self):
        return (cell for cell in self.__coordinates())