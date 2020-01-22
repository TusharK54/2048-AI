
import tkinter as tk
import numpy as np
import abc

from game.game import Move, GameState

class ViewModel(abc.ABC):
    """A mostly read-only model for the view."""

    def __init__(self, board: GameState=None):
        self.board = board
        self.size = tk.IntVar()
        self.score = tk.IntVar()
        self.best = tk.IntVar()
        self.ai = False

    def get_board(self) -> GameState:
        """Return a `GameState` object with a copy of the state of the board."""
        return self.board.copy()

    def get_size_var(self) -> tk.IntVar:
        """Return a `tk.IntVar` object containing the grid size."""
        return self.size

    def get_score_var(self) -> tk.IntVar:
        """Return a `tk.IntVar` object containing the current game score."""
        return self.score

    def get_best_var(self) -> tk.IntVar:
        """Return a `tk.IntVar` object containing the best game score."""
        return self.best

    def get_grid(self) -> np.ndarray:
        """Return a matrix of the game tiles."""
        return self.board.get_matrix()

    def get_game_over(self) -> bool:
        """Return `True` only if the game is over."""
        return self.board.game_over()

    def get_ai(self) -> bool:
        """Return `True` only if an AI is enabled."""
        return self.ai

    def __repr__(self) -> str:
        return str(self.board.matrix)

class ControlModel(ViewModel):
    """A writeable model for the controller."""

    def __init__(self):
        ViewModel.__init__(self)
        self.new_game()

    def new_game(self, size: int=None):
        default_board = GameState() if self.size.get() == 0 else GameState(self.size.get())
        self.board = default_board if size is None else GameState(size)
        self.update_vars()

    def update_vars(self):
        self.size.set(self.board.get_size())
        self.score.set(self.board.get_score())
        if self.score.get() > self.best.get():
            self.best.set(self.score.get())

    def set_ai(self, new: bool):
        self.ai = new

    def move_tiles(self, direction: Move) -> bool:
        """Push tiles in the specified direction and return whether that was a valid move."""
        validity = self.board.valid_move(direction)
        self.update_vars()
        return validity
