
import random
from game.game import Move, Board

from base import Player

class RandomPlayer(Player):
    
    def get_move(self, state: Board) -> Move:
        moves = [m for m in Move]
        return random.choice(moves)