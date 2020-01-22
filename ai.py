
from threading import Thread
from abc import ABC, abstractmethod
from random import shuffle

from pub_sub import Publisher
from game import Move, GameState

class Base(object):

    def __init__(self, game: GameState):
        self.update_state(game)

    def update_state(self, game: GameState):
        self.game_state = game

    def evaluate_move(self, move: Move) -> float:
        """Return a value in the interval [0, 1] representing the AI's evaluation of applying `move` to the current game state."""
        if not self.game_state.valid_move(move):
            return 0
        

class BasePlayer(ABC):

    def __init__(self, game: GameState):
        self.update_state(game)

    def update_state(self, game: GameState):
        self.game_state = game

    def make_next_move(self) -> Move:
        move = self.get_next_move()
        self.update_state(self.game_state.next_state(move))
        return move

    def get_game_state(self) -> GameState:
        return self.game_state

    @abstractmethod
    def get_next_move(self) -> Move:
        """Return a move, which is guarunteed to be valid. Requires that the game isn't over."""
        pass

class RandomPlayer(BasePlayer):

    def get_next_move(self):
        moves = [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT]
        shuffle(moves)

        move = moves.pop()
        while not self.game_state.valid_move(move) and len(moves) > 0:
            move = moves.pop()

        return move