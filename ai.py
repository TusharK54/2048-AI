
from threading import Thread
from abc import ABC, abstractmethod
from random import choice

from game import Move, GameState
from pub_sub import QueueManager

class BaseAI(ABC):

    def __init__(self, game: GameState):
        self.game_state = game

    def make_move(self, move: Move=None) -> Move:
        """Update the game state by applying `move` or picking the best valid move as determined by `self.evaluate_move`. Returns the move made."""
        if move is None:
            # Generate a list of the highest-evaluated moves
            best_evaluation, best_moves = None, []            
            for move in Move:
                if not self.game_state.valid_move(move):
                    continue

                evaluation = self.evaluate_move(move)
                if best_evaluation is None or evaluation > best_evaluation:
                    best_evaluation = evaluation
                    best_moves = [move]
                elif evaluation == best_evaluation:
                    best_moves.append(move)

            # Deterministically pick a highest-evaluated move
            move = best_moves[0]

        self.game_state.update_state(move)
        return move

    @abstractmethod
    def evaluate_move(self, move: Move) -> int:
        """Return a value representing the AI's evaluation of applying `move` to the current game state."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Return the name of this AI."""
        pass
        
class DummyAI(BaseAI):

    def evaluate_move(self, move) -> int:
        val = 0
        for tile in self.game_state.next_state(move).get_matrix().flatten():
            if tile != 0:
                val += tile ** 2
        return val

    def __str__(self):
        return 'dummy 1'

class SearchTreeAI(BaseAI):

    def evaluate_move(self, move) -> int:
        pass

    def __str__(self):
        return 'Search Tree'