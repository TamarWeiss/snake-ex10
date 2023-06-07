SNAKE_SIZE = 3
GROW_BONUS = 3

SNAKE_COLOR = 'black'
APPLE_COLOR = 'green'
WALL_COLOR = 'blue'

LEFT = 'Left'
RIGHT = 'Right'
DOWN = 'Down'
UP = 'Up'

# a dictionary which maps an inverse direction to each direction
inverse_directions = {
    LEFT: RIGHT,
    RIGHT: LEFT,
    DOWN: UP,
    UP: DOWN
}

Point = tuple[int, int]