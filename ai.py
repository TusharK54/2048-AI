
from threading import Thread
from abc import ABC, abstractmethod
from random import shuffle

from pub_sub import Publisher
from game import Move, Game

class BasePlayer(ABC):

    def __init__(self, state: Game):
        self.update_state(state)

    def update_state(self, state: Game):
        self.state = state

    def make_next_move(self) -> Move:
        move = self.get_next_move()
        self.state.make_move(move)
        return move

    def get_game_state(self) -> Game:
        return self.state

    @abstractmethod
    def get_next_move(self) -> Move:
        """Return a move, which is guarunteed to be valid. Requires that the game isn't over."""
        pass

class RandomPlayer(BasePlayer):

    def get_next_move(self):
        moves = [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT]
        shuffle(moves)

        move = moves.pop()
        while not self.state.valid_move(move) and len(moves) > 0:
            move = moves.pop()

        return move