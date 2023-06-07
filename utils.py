from consts import DOWN, LEFT, RIGHT, UP

Location = tuple[int, int]

def check_inbounds(num: int, length: int):
    return 0 <= num < length

def get_next_pos(head: Location, direction: str) -> Location:
    x, y = head
    x += -int(direction == LEFT) + int(direction == RIGHT)
    y += -int(direction == DOWN) + int(direction == UP)
    return x, y