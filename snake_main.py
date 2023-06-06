import argparse

from game_display import GameDisplay
from snake_game import SnakeGame

def main_loop(gd: GameDisplay, args: argparse.Namespace) -> None:
    game = SnakeGame(gd, args)  # INIT OBJECTS
    game.draw_board()  # DRAW BOARD
    game.end_round()
    # END OF ROUND 0
    while not game.is_over():
        game.read_key()  # CHECK KEY CLICKS
        game.update_objects()  # UPDATE OBJECTS
        game.draw_board()  # DRAW BOARD
        game.end_round()  # WAIT FOR THE NEXT ROUND:
    game.game_over()

if __name__ == "__main__":
    print("You should run:\n"
          "> python game_display.py")