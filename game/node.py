
from board import Board

class BoardNode:

    def __init__(self, board: Board):
        self.board = board
        self.depth = 0
        self.move = None
        self.parent = None
        self.score = self._get_heuristic_score()

    def generate_children(self) -> list:
        self.children = []
        for move in [Board.UP, Board.DOWN, Board.LEFT, Board.RIGHT]:
            child = BoardNode(self.board.deterministic_copy())
            child.set_parent(self)
            child.board.move(move)
            child.move = move
            if child.board.valid_last_move:
                self.children.append(child)
        return self.children

    def set_parent(self, parent):
        self.parent = parent
        self.depth = parent.depth + 1

    def _get_heuristic_score(self) -> int:
        score = self.board.score
        clear_tiles = len([(i,j) for i in range(self.board.size) for j in range (self.board.size) if self.board.tilemap[i][j] == 0])
        return score + clear_tiles

if __name__ == '__main__':
    board = Board()
    node = BoardNode(board)

    node.generate_children()