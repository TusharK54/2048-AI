
from board import Board
from node import BoardNode

from random import choice

class MoveTree:

    def __init__(self, board:Board, iterations=5):
        self.board = board
        self.iterations = iterations
        self.root = BoardNode(board)

        # Generate move tree and compute leafs
        self.leafs = [self.root]
        while len(self.leafs) > 0 and self.leafs[0].depth < self.root.depth + self.iterations:
            leaf = self.leafs.pop(0)
            self.leafs += leaf.generate_children()

    def get_best_move(self):
        best_leafs = []
        best_score = 0
        for leaf in self.leafs:
            if leaf.score == best_score:
                best_leafs.append(leaf)
            elif leaf.score > best_score:
                best_leafs = [leaf]
                best_score = leaf.score

        node = choice(best_leafs)
        while node.parent != self.root:
            node = node.parent
        return node.move

    def update_board(self, move):
        # Change root of tree and update leafs
        for index in range(len(self.root.children)):
            if self.root.children[index].move == move:
                self.root = self.root.children[index]

                leftmost_leaf, rightmost_leaf = self.root, self.root
                while leftmost_leaf.children != []:
                    leftmost_leaf = leftmost_leaf.children[0]
                while rightmost_leaf.children != []:
                    rightmost_leaf = rightmost_leaf.children[len(rightmost_leaf.children)-1]
                left_index = self.leafs.index(leftmost_leaf)
                right_index = self.leafs.index(rightmost_leaf, left_index)
                self.leafs = self.leafs[left_index:right_index+1]
                break

        # Recompute bottom layer of tree by getting children of current leafs
        leaf_children = []
        for node in self.leafs:
            leaf_children += node.generate_children()
        self.leafs = leaf_children

if __name__ == '__main__':

    import time

    board = Board(4)
    board.pretty_print()

    iterations = 4
    AI = MoveTree(board, iterations)

    update_time = 0
    for i in range(10):
        
        next_move = AI.get_best_move()     
        board.move(next_move)

        print(f'{i+1}th move - {len(AI.leafs)} leafs:')
        board.pretty_print()

        t = time.time_ns()
        AI.update_board(next_move)
        #AI = MoveTree(board, iterations)
        t = time.time_ns() - t
        update_time += t

    print(f'DONE in {update_time*10**-9} seconds')