
from game.game import Move, GameState
from abc import ABC, abstractmethod

class Player(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_move(self, board: GameState) -> Move:
        """Return the move the player makes in the given `state`.
        Not guarunteed to be a valid move."""
        pass