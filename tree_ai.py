
from abc import abstractmethod
import numpy as np

from ai import BaseAI
from game import Move, GameState
from messaging import QueueHandler, UnknownEventError

import time

class GameNode(object):
    """Stores game state as data."""

    def __init__(self, game: GameState=None, parent: GameState=None, move: Move=None):
        """A node representing a game state, where `move` is how `game` can be reached from `parent`.
        The value for `game` can be omitted if a value for both `parent` and `move` are provided."""
        if game is not None:
            self.game_state = game
        else:
            assert parent.game_state.valid_move(move)
            self.game_state = parent.game_state.next_state(move)

        self.parent = parent
        self.move = move
        self.move_history = np.empty(0) if parent is None else np.append(parent.move_history, move) # numpy.ndarray for performance
        self.children = None

    def get_children(self) -> list:
        """Returns the children of this node in a list."""
        if self.children is None:
            self.children = [GameNode(parent=self, move=m) for m in Move if self.game_state.valid_move(m)]
        return self.children

    def __repr__(self):
        """For testing purposes."""
        return f'move: {self.move}, history: {self.move_history}\n{self.game_state}'

class GameTree(QueueHandler):
    """Represents a game search tree that uses background threads to continually grow."""

    def __init__(self, game: GameState):
        BaseAI.__init__(self, game)
        QueueHandler.__init__(self)

        self.root = GameNode(game)
        self.leaves = np.asarray([self.root]) # numpy.ndarray for performance

        self.launch_thread()

    def get_leaves(self) -> np.ndarray:
        """Return the leaves of the tree as a numpy.ndarray."""
        return self.leaves

    def get_depth(self) -> int:
        """Returns the depth of the tree."""
        return self.get_leaves()[-1].move_history.size - self.root.move_history.size

    def update(self, move: Move):
        """Update the tree by making the move defined by `move`. Requires that `move` is a valid move."""
        self.root = {child.move: child for child in self.root.get_children()}[move]
        
        # Trim out unreachable nodes using the move history of the root
        move_filter = np.vectorize(lambda x: np.array_equal(x.move_history[:self.root.move_history.size], self.root.move_history))
        self.leaves = self.leaves[move_filter(self.leaves)]
        if self.leaves.size == 0: self.leaves = np.asarray([self.root])

    def handle_event(self, event, data):
        if event == 'autogrow': # data is number of leafs
            self.grow()
            self.queue('autogrow', self.get_leaves().size)
        else:
            raise UnknownEventError

    def launch_thread(self):
        QueueHandler.launch_thread(self)
        self.queue('autogrow', self.get_leaves().size) # Launch the auto-growing mechanism

    def grow(self):
        """Grows the tree by generating the children of a single leaf."""
        child = self.leaves[0]
        self.leaves = np.append(np.delete(self.leaves, 0), child.get_children())

class Heuristics(object):
    """Defines different heuristic evaluation functions for game states."""

    @staticmethod
    def basic_evaluate(game: GameState) -> int:
        return game.get_score()

class TreeSearchAI(BaseAI):

    def __init__(self, game: GameState):
        BaseAI.__init__(self, game)
        self.tree = GameTree(game)

    def make_move(self, move: Move=None):
        move = BaseAI.make_move(self, move)
        # TODO update root and tree

    def evaluate_move(self, move: Move) -> int:
        move_filter = np.vectorize(lambda x: np.array_equal(x.move_history[:self.tree.root.move_history.size+1], np.append(self.tree.root.move_history, move)))
        leaves = self.tree.get_leaves()[move_filter(self.tree.get_leaves())]
        # TODO get max value of `leaves`
        pass

    def __str__(self) -> str:
        return "Tree Search"

if __name__ == '__main__':
    t = GameTree(GameState(4))

    TIME_FREQ = 10 # number of times to check depth per second
    depth = 5
    
    start = time.time_ns()
    while t.get_depth() < depth+1: 
        time.sleep(1/TIME_FREQ)
    end = time.time_ns()

    leaves, depth, time, rate = t.get_leaves().size, t.get_depth()-1, int((end-start) * 10 ** -9 * TIME_FREQ)/TIME_FREQ, 0
    print(f'DONE: Generated a tree of depth {depth} with {leaves} leaves in ~{time} seconds @ {round(leaves/time,2)} leaves/sec.')