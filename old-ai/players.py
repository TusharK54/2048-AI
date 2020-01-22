
import random
from game.game import Move, GameState

from .base import Player

class RandomPlayer(Player):
    
    def get_move(self, state: GameState) -> Move:
        moves = [m for m in Move]
        return random.choice(moves)


class StateNode(object):

    def __init__(self, board: GameState, parent=None):
        self.board = board
        self.parent = parent
        self.children = None

    def get_children(self) -> list:
        """Generate and return this node's children."""
        if self.children is None:
            self.children = {}
            for m in Move:
                if self.board.valid_move(m):
                    child = StateNode(self.board.next_move(m), parent=self)
                    self.children[m] = child
        
        return list(self.children.values())

    def get_move(self, child) -> Move:
        for move in self.children.keys():
            if self.children.get(move) == child:
                return move
        return None

    def get_child(self, move):
        return self.children.get(move)

    def __eq__(self, other):
        return self.board == other.board

    def __str__(self):
        s = str(self.board) 
        if self.parent is not None:
            s += ' ' + str(self.parent.get_move(self))
        return s

class SearchTree(Player):

    def __init__(self):
        self.root = None

        self.depth = 3

    def get_move(self, board: GameState) -> Move:
        pass
        
    def find_node(self, board: GameState):
        search = StateNode(board)
        frontier = [self.root]
        while len(frontier) > 0:
            node = frontier.pop()
            if node == search:
                return node
            else:
                frontier.extend(node.get_children())
        return None

    def generate_tree(self, root: StateNode, depth: int):
        """Generates the search tree and returns the leaves."""
        leaves = [root]
        for _ in range(depth):
            new_leaves = []
            for node in leaves:
                new_leaves.extend(node.get_children())
            leaves = new_leaves
        return leaves

    def __repr__(self):
        s = ''
        stack = [self.root]

        i = 0
        while len(stack) > 0:
            node = stack.pop()
            if node is None:
                s += '\n'
            else:
                s += '- - - O'
                stack.extend(node.get_children())
        return s

if __name__ == '__main__':
    board = GameState()

    node = StateNode(board)
    tree = SearchTree()

    tree.generate_tree(node, 3)
    print(tree)