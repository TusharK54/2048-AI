
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
        while len(self.leafs) > 0:
            leaf_children = []
            for node in self.leafs:
                    leaf_children += node.generate_children()
            
            if len(leaf_children) > 0:
                self.leafs = leaf_children
                if self.leafs[0].depth == self.root.depth + self.iterations:
                    break
            else:
                break

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
                self.root.parent = None

                leftmost_leaf_queue = [self.root]
                while len(leftmost_leaf_queue) > 0 and leftmost_leaf_queue[0].depth < self.root.depth + self.iterations - 1:
                    node = leftmost_leaf_queue.pop(0)
                    leftmost_leaf_queue = node.children + leftmost_leaf_queue
                leftmost_leaf = leftmost_leaf_queue.pop(0)

                rightmost_leaf_queue = [self.root]
                while len(rightmost_leaf_queue) > 0 and rightmost_leaf_queue[len(rightmost_leaf_queue)-1].depth < self.root.depth + self.iterations - 1:
                    node = rightmost_leaf_queue.pop()
                    rightmost_leaf_queue += node.children
                rightmost_leaf = rightmost_leaf_queue.pop()

                left_index = self.leafs.index(leftmost_leaf)
                right_index = self.leafs.index(rightmost_leaf, left_index)
                self.leafs = self.leafs[left_index:right_index+1]
                break

        # Recompute bottom layer of tree by getting children of current leafs
        leaf_children = []
        for node in self.leafs:
            leaf_children += node.generate_children()
        if len(leaf_children) > 0:
            self.leafs = leaf_children
        else:
            self.iterations -= 1

if __name__ == '__main__':

    import time

    board = Board(4)
    board.pretty_print()

    iterations = 5
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