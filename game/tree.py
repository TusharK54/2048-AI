
from board import Board
from node import BoardNode

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
        best_leaf = None
        for leaf in self.leafs:
            if best_leaf == None or best_leaf.score < leaf.score:
                best_leaf = leaf

        node = best_leaf
        while node.parent != self.root:
            node = node.parent
        return node.move

    #TODO: FIX (not working)
    def update_root(self, move):
        branch_size = len(self.leafs) / len(self.root.children)

        # Change root of tree and update leafs
        for index in range(len(self.root.children)):
            if self.root.children[index] == move:
                self.root = self.root.children[index]
                self.leafs = self.leafs[index*branch_size:(index+1)*branch_size]
                break

        # Recompute bottom layer of tree by getting children of current leafs
        leaf_children = []
        for node in self.leafs:
            leaf_children += node.generate_children()
        self.leafs = leaf_children

if __name__ == '__main__':

    board = Board(4)
    board.pretty_print()

    iterations = 4
    AI = MoveTree(board, iterations)

    for i in range(1000):
        print(i+1, end='th move:\n')
        next_move = AI.get_best_move()     
        board.move(next_move)
        board.pretty_print()

        #AI.update_root(next_move)
        AI = MoveTree(board, iterations)

    print("DONE")