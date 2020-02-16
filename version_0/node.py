
from board import GameState

class BoardNode:

    def __init__(self, board: GameState):
        self.board = board
        self.depth = 0
        self.move = None
        self.parent = None
        self.children = []

    def generate_children(self) -> list:
        self.children = []
        for move in [GameState.UP, GameState.DOWN, GameState.LEFT, GameState.RIGHT]:
            child = BoardNode(self.board.deterministic_copy())
            child._set_parent(self)
            child.board.move(move)
            child.move = move
            if child.board.valid_last_move:
                self.children.append(child)
        return self.children            

    def _set_parent(self, parent):
        self.parent = parent
        self.depth = parent.depth + 1

    def get_evaluation_score(self) -> int:
        score = self.board.score
        clear_tiles = 0
        best_tile = 0
        for row in self.board.tilemap:
            for tile in row:
                if tile == 0:
                    clear_tiles += 1
                if tile > best_tile:
                    best_tile = tile
        return score * clear_tiles * best_tile

if __name__ == '__main__':
    board = GameState()
    node = BoardNode(board)

    node.generate_children()