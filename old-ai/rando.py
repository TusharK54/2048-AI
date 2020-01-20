
import random
from game.game import Move, Game

from base import Player

class RandomPlayer(Player):
    
    def get_move(self, state: Game) -> Move:
        moves = [m for m in Move]
        return random.choice(moves)