import argparse
import sys
import threading
import time
import tkinter as tki
from argparse import Namespace
from typing import Callable, Optional

import game_utils
from consts import Point, inverse_directions

CELL_SIZE = 15
ROUND_TIME = 150

WIDTH = 40
HEIGHT = 30
NUM_OF_APPLES = 3
NUM_OF_WALLS = 2

Pixel = tuple[int, int, str]

class GameDisplay:
    def __init__(self, width: int, height: int, delay: int, verbose: int, args: Namespace):
        """Creates a new game display object and initializes it"""
        import snake_main  # placed this import in here to solve circular import issues.
        self.width, self.height, self.delay, self.verbose = width, height, delay / 1000, verbose > 1
        self._round_num = 0
        self._root = tki.Tk()
        self._root.title('Snake')
        self._root.bind('<KeyPress>', self._key_press)
        self._score_var = tki.StringVar()

        self._init_score_frame()
        self._canvas = tki.Canvas(self._root, bg="white", width=self.width * CELL_SIZE, height=self.height * CELL_SIZE)
        self._canvas.pack()
        self._to_draw: dict[Point, str] = {}
        self._already_drawn: dict[Pixel, int] = {}

        self._root.resizable(False, False)
        self.key_click: Optional[str] = None
        self._key_click_round: int = 0

        self._game_control_thread = threading.Thread(target=snake_main.main_loop, args=(self, args))
        self._game_control_thread.daemon = True
        self._round_start_time = time.time()

    def _init_score_frame(self):
        """
        Internal: This method initializes the score frame
        :return: None
        """
        self._score_frame = tki.Frame(self._root)
        self._score_frame.pack(side=tki.TOP)

        self.show_score("Not Set")
        self._score_label = tki.Label(self._score_frame, borderwidth=2, relief="ridge",
            textvariable=self._score_var, font=("Courier", 22))

        self._score_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self._score_frame.grid_rowconfigure(0, weight=1)

    def start(self):
        """
        Internal: Starts the program: calls the main method and runs the GUI.
        :return: None
        """
        self._root.after(500, self._game_control_thread.start)
        self._root.after(1000, self._check_end)
        self._root.mainloop()

    def _check_end(self):
        """
        Internal: This method checks if the game has finished
        :return: None
        """
        is_alive = self._game_control_thread.is_alive()
        args: tuple[int, Callable] = (2000, self._root.destroy) if not is_alive else (300, self._check_end)
        self._root.after(*args)

    def _key_press(self, e: tki.Event):
        """
        Internal: checks which key was clicked in the event.
        :param e:Event
        :return:None
        """
        if e.keysym in inverse_directions:
            self.key_click = e.keysym
            self._key_click_round = self._round_num

    def get_key_clicked(self) -> Optional[str]:
        """
        This method returns which key is clicked
        and also turns off the key clicked FLAG
        :return: None, or one of 'Left', 'Right', 'Up', 'Down'
        """
        result = self.key_click
        self.key_click = None
        return result

    def draw_cell(self, x: int, y: int, color: str):
        """
        Sets the cell at the given coordinates to draw in given color
        :param x: coordinate at x
        :param y: coordinate at y
        :param color: the color we wish to draw
        :return: None
        """
        self._to_draw[x, y] = color

    def _check_inbounds(self, x: int, y: int) -> bool:
        def check_inbounds_helper(num: int, length: int) -> bool:
            return 0 <= num < length
        return check_inbounds_helper(x, self.width) and check_inbounds_helper(y, self.height)

    def _buffer_draw_cell(self, x: int, y: int, color: str) -> int:
        """
        Internal: internal method to draw the x,y cell in color
        :param x: coordinate at x
        :param y: coordinate at y
        :param color: the color we wish to draw
        :return: None
        """
        if not self._check_inbounds(x, y):
            raise ValueError(f"cell index out of bounds of the board: {(x, y)}")
        # setting the coordinates of the board correctly,
        # the y-axis needs to point up.
        # the following line adjusts this.
        y = self.height - y
        return self._canvas.create_rectangle(
            x * CELL_SIZE, (y - 1) * CELL_SIZE,
            (x + 1) * CELL_SIZE, y * CELL_SIZE,
            fill=color, outline=color)

    def _update_drawing(self):
        """
        Internal: method to update drawing
        :return: None
        """
        self.verbose and print(self._to_draw)
        to_draw = {(x, y, color) for (x, y), color in self._to_draw.items()}
        for rect in self._already_drawn:
            rect not in to_draw and self._canvas.delete(self._already_drawn[rect])

        cur_drawn: dict[Pixel, int] = {}
        for (x, y), color in self._to_draw.items():
            ind = self._already_drawn.get((x, y, color), None)
            if ind is None:
                ind = self._buffer_draw_cell(x, y, color)
            cur_drawn[(x, y, color)] = ind

        self._already_drawn = cur_drawn
        self._to_draw = {}

    def end_round(self):
        """
        This method ends the current round.
        :return:None
        """
        self._update_drawing()

        self._round_start_time += self.delay
        now = time.time()
        while now < self._round_start_time:
            time.sleep(self._round_start_time - now)
            now = time.time()
        self._round_num += 1

    def show_score(self, val):
        """
        This method updates the currently shown score on the board.
        :param val: The score we wish to display
        :return: None
        """
        score = f'Score:{val}'
        self.verbose and print(score)
        self._score_var.set(score)

def parse_args(argv: list[str]) -> Namespace:
    parser = argparse.ArgumentParser(prog='game_display.py', description='Runs snake game')
    parser.add_argument('-x', '--width', type=int, default=WIDTH, help='args.width: Game board width')
    parser.add_argument('-y', '--height', type=int, default=HEIGHT, help='args.height: Game board height')
    parser.add_argument('-s', '--seed', default=None, help='Seed for random number generator (not passed to game loop)')
    parser.add_argument('-a', '--apples', type=int, default=NUM_OF_APPLES, help='args.apples: Number of apples')
    parser.add_argument('-d', '--debug', action='store_true', help='args.debug: Debug mode with no snake')
    parser.add_argument('-w', '--walls', type=int, default=NUM_OF_WALLS, help='args.walls: Number of walls')
    parser.add_argument('-r', '--rounds', type=int, default=-1, help='args.rounds: Number of rounds')
    parser.add_argument('-t', '--delay', type=int, default=ROUND_TIME,
        help='Delay between rounds in milliseconds (not passed to game loop)')
    parser.add_argument('-v', '--verbose', action='count', default=0,
        help='Print helpful debugging information (not passed to game loop, can be used multiple times)')
    return parser.parse_args(argv)

def setup_game(args: Namespace) -> GameDisplay:
    game_utils.set_random_seed(args.__dict__.pop('seed'))
    game_utils.set_verbose(args.verbose)
    game_utils.set_size(args.width, args.height)
    return GameDisplay(args.width, args.height, args.__dict__.pop('delay'), args.__dict__.pop('verbose'), args)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    gd = setup_game(args)
    gd.start()