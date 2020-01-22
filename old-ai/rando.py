
import random
from game.game import Move, GameState

from base import Player

class RandomPlayer(Player):
    
    def get_move(self, state: GameState) -> Move:
        moves = [m for m in Move]
        return random.choice(moves)