from game import Board

def get_heuristic_score(board: Board) -> int:
    score = board.score
    clear_tiles = len([(i,j) for i in range(board.size) for j in range (board.size) if board.tilemap[i][j] == 0])
    return score + clear_tiles

def next_moves(board: Board) -> list:
    children = [board.deterministic_copy(), board.deterministic_copy(), board.deterministic_copy(), board.deterministic_copy()]
    children[0].move('UP')
    children[1].move('DOWN')
    children[2].move('LEFT')
    children[3].move('RIGHT')
    return [child for child in children if child.valid_last_move]

class Bot:

    def __init__(self, board: Board, iterations=5):
        self.board = board
        self.iterations = iterations
        self.leafs = [{'board' : self.board, 'n' : 0, 'score' : get_heuristic_score(self.board)}]

        # Generate moves tree
        while (self.leafs[0]['n'] < self.iterations):
            leaf = self.leafs.pop(0)
            for child in next_moves(leaf['board']):
                self.leafs.append({'board' : child, 'n' : leaf['n']+1, 'score' : get_heuristic_score(child)})

    def get_best_move(self):
        pass
        
class Node:

    def __init__(self, board: Board, depth: int, score: int):
        self.board = board
        self.depth = depth
        self.score = score

    def add_children(self, children: list):
        self.children = children


if __name__ == '__main__':

    b = Board()
    b.reset()
    b.move('UP')
    b.move('DOWN')

    b.pretty_print()
    n = next_moves(b)
    b.pretty_print()

    n[3].pretty_print()

    b.move('UP')
    b.pretty_print()

