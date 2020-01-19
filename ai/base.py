
from game.game import Move, Board
from abc import ABC, abstractmethod

class Player(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_move(self, board: Board) -> Move:
        """Return the move the player makes in the given `state`.
        Not guarunteed to be a valid move."""
        pass