
from enum import Enum, auto
import numpy as np
import random

class Move(Enum):
    UP, DOWN, LEFT, RIGHT = 3, 1, 0, 2

class GameState(object):

    def __init__(self, size=4):
        assert size != 0, 'size cannot be 0'
        self.matrix = np.zeros((size, size), dtype=np.uint32)
        self.spawn_4_chance = 0.1
        self.score = 0
        self.random_state = random.getstate()

        self.spawn_tile()

    def copy_state(self, other):
        """Update this game state to the game state of `other`."""
        self.matrix = other.matrix.copy()
        self.spawn_4_chance = other.spawn_4_chance
        self.score = other.score
        self.random_state = other.random_state

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
        """Return whether `move` slides any tiles."""
        return self != self.next_state(move)

    def update_state(self, move: Move):
        """Update this game state to the next game state."""
        self.copy_state(self.next_state(move))

    def next_state(self, move: Move):
        """Return the next game state."""
        new_matrix, points = self.slide_tiles(move)
        
        if points == 0 and np.array_equal(self.matrix, new_matrix):
            return self

        new_state = GameState()
        new_state.copy_state(self)
        new_state.matrix = new_matrix
        new_state.score += points
        new_state.spawn_tile()

        return new_state

    def slide_tiles(self, move: Move) -> tuple:
        """Translate and combine tiles in the specified direction if possible and return the tuple `(matrix, points)`."""
        matrix = self.matrix.copy()
        matrix = np.rot90(matrix, -move.value)
        points = 0

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
                        row[j], row[i] = 0, row[j]
                    elif row[i] == row[j]:
                        row[j], row[i], flag = 0, row[i]*2, True
                        points += row[i]
                    else:
                        flag = True


        matrix = np.rot90(matrix, move.value)
        return matrix, points

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
    game = GameState()

    while not game.game_over():
        print(game)
        move = input('Input next move [WASD]: ').lower()
        if move == 'w':
            game = game.next_state(Move.UP)
        elif move == 'a':
            game = game.next_state(Move.LEFT)
        elif move == 's':
            game = game.next_state(Move.DOWN)
        elif move == 'd':
            game = game.next_state(Move.RIGHT)
        else:
            print('Please use the WASD keys')

    print('\nGame Over!')
    print('Final Score:', game.get_score())