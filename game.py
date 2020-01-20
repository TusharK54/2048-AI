
from enum import Enum, auto
import numpy as np
import random

class Move(Enum):
    UP, LEFT, DOWN, RIGHT = 3, 0, 1, 2

class Game(object):

    def __init__(self, size=4, copy=None):
        if copy is None:
            self.matrix = np.zeros((size, size), dtype=np.uint32)
            self.spawn_4_chance = 0.1
            self.score = 0
            self.random_state = random.getstate()
            self.spawn_tile()

        else:
            self.matrix = copy.matrix.copy()
            self.spawn_4_chance = copy.spawn_4_chance
            self.score = copy.score
            self.random_state = copy.random_state

    def copy(self, matrix=None):
        """Return a deep copy of this object."""
        new = Game(copy=self)
        if matrix is not None:
            new.matrix = matrix
        return new

    def get_size(self) -> int:
        return len(self.matrix)

    def get_score(self) -> int:
        return self.score

    def get_tile(self, row: int, col: int) -> int:
        """Return the value of the tile at the specified position."""
        return self.matrix[row][col]
        
    def get_matrix(self) -> np.ndarray:
        """Return a copy of the tiles as a NumPy `ndarray`."""
        return self.matrix.copy()

    def game_over(self) -> bool:
        """Return `True` only if there are no more valid moves remaining."""
        if np.count_nonzero(self.matrix) < self.matrix.size:
            return False

        for move in Move:
            if self.valid_move(move):
                return False

        return True

    def valid_move(self, move: Move) -> bool:
        """Return whether `move` is a valid move."""
        new_matrix = self.slide_matrix(move)
        return not np.array_equal(self.matrix, new_matrix)

    def make_move(self, move: Move) -> bool:
        """Make a move on the board and return whether it was a valid move."""
        new_matrix = self.slide_matrix(move)

        if np.array_equal(self.matrix, new_matrix):
            return False

        self.matrix = new_matrix
        self.spawn_tile()
        return True

    def next_move(self, move: Move):
        """Return a copy of the next game state without affecting this one."""
        new_matrix = self.slide_matrix(move)
        copy = self.copy(matrix=new_matrix)
        copy.spawn_tile()
        return copy

    def slide_matrix(self, move: Move) -> np.ndarray:
        """Translate and combine tiles in the specified direction if possible and return the new matrix."""
        matrix = self.matrix.copy()
        matrix = np.rot90(matrix, -move.value)

        # collapse and merge tiles to the LEFT
        # O(n^2) run-time
        for row in matrix:
            for i in range(len(row)):
                flag = False
                for j in range(i+1, len(row)):
                    if flag:
                        break
                    elif row[j] == 0:
                        continue
                    elif row[i] == 0 and row[j] != 0:
                        row[i] = row[j]
                        row[j] = 0
                    elif row[i] == row[j]:
                        row[i] = row[i]*2
                        row[j] = 0
                        flag = True
                    else:
                        flag = True

        matrix = np.rot90(matrix, move.value)
        return matrix

    def spawn_tile(self):
        clear_tiles = [(i,j) for i in range(len(self.matrix)) for j in range(len(self.matrix)) if self.matrix[i][j] == 0]
        
        random.setstate(self.random_state)
        row, col = random.choice(clear_tiles)
        self.matrix[row][col] = 2 if random.random() >= self.spawn_4_chance else 4
        self.random_state = random.getstate()

    def __eq__(self, other):
        return np.array_equal(self.matrix, other.matrix) and \
            self.spawn_4_chance == other.spawn_4_chance and \
            self.score == other.score and \
            self.random_state == other.random_state

    def __str__(self):
        return str(self.matrix)

if __name__ == '__main__':
    game = Game()

    while not game.game_over():
        print(game)
        move = input('Input next move [WASD]: ').lower()
        if move == 'w':
            game.make_move(Move.UP)
        elif move == 'a':
            game.make_move(Move.LEFT)
        elif move == 's':
            game.make_move(Move.DOWN)
        elif move == 'd':
            game.make_move(Move.RIGHT)
        else:
            print('Please use the WASD keys')

    print('\nGame Over!')
    print('Final Score:', game.get_score())