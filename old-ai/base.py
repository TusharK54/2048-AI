
from game.game import Move, Game
from abc import ABC, abstractmethod

class Player(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_move(self, board: Game) -> Move:
        """Return the move the player makes in the given `state`.
        Not guarunteed to be a valid move."""
        pass