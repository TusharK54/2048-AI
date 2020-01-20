
import unittest

import numpy as np
from game import Move, Game

class GameTests(unittest.TestCase):
    
    def setUp(self):
        self.state = Game()

    def compare_row(self, before, expected):
        # Test LEFT
        self.state.matrix[0] = before
        new_board = self.state.slide_matrix(Move.LEFT)
        after = new_board[0]

        self.assertTrue(np.array_equal(after, expected), f'\nFailed LEFT test\nActual: { after }\nExpected: { expected }')

        # Test RIGHT
        self.state.matrix[0] = np.flip(before)
        new_board = self.state.slide_matrix(Move.RIGHT)
        after = np.flip(new_board[0])
        
        self.assertTrue(np.array_equal(after, expected), f'\nFailed RIGHT test\nActual: { after }\nExpected: { expected }')

        # Test UP
        self.state.matrix[0] = before
        matrix = self.state.matrix
        matrix = np.rot90(matrix, -1)
        self.state.matrix = matrix
        matrix = self.state.slide_matrix(Move.UP)
        matrix = np.rot90(matrix, 1)
        after = matrix[0]

        self.assertTrue(np.array_equal(after, expected), f'\nFailed UP test\nActual: { after }\nExpected: { expected }')

        # Test DOWN
        self.state.matrix[0] = before
        matrix = self.state.matrix
        matrix = np.rot90(matrix, 1)
        self.state.matrix = matrix
        matrix = self.state.slide_matrix(Move.DOWN)
        matrix = np.rot90(matrix, -1)
        after = matrix[0]

        self.assertTrue(np.array_equal(after, expected), f'\nFailed DOWN test\nActual: { after }\nExpected: { expected }')

    def test(self):
        before   = [0, 0, 2, 2]
        expected = [4, 0, 0, 0]
        self.compare_row(before, expected)

    def test2(self):
        before   = [0, 2, 0, 2]
        expected = [4, 0, 0, 0]
        self.compare_row(before, expected)

    def test3(self):
        before   = [2, 2, 4, 4]
        expected = [4, 8, 0, 0]
        self.compare_row(before, expected)
        
    def test4(self):
        before   = [4, 2, 4, 4]
        expected = [4, 2, 8, 0]
        self.compare_row(before, expected)

    def test5(self):
        before   = [8, 2, 4, 2]
        expected = [8, 2, 4, 2]
        self.compare_row(before, expected)

    def test6(self):
        before   = [0, 2, 4, 4]
        expected = [2, 8, 0, 0]
        self.compare_row(before, expected)

    def test7(self):
        before   = [4, 0, 2, 2]
        expected = [4, 4, 0, 0]
        self.compare_row(before, expected)

    def test8(self):
        before   = [2, 2, 2, 2]
        expected = [4, 4, 0, 0]
        self.compare_row(before, expected)

if __name__ == '__main__':
    unittest.main()