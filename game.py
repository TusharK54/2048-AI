import random

class Board:

    def __init__(self, size=4):
        self.size = size
        self._spawn_4_probability = 0.1
        self.valid_last_move = False
        self._random_state = random.getstate()
        self.reset()

        # Track how many tiles each tile moved in the last turn for transition animation
        self._slidemap = [[0 for i in range(self.size)] for j in range(self.size)]
        self._mergemap = [[0 for i in range(self.size)] for j in range(self.size)]

    def reset(self):
        self.tilemap = [[0 for i in range(self.size)] for j in range(self.size)]
        self.score = 0
        self.spawn_tile()

    def copy(self):
        board = Board()
        board.size = self.size
        board.score = self.score
        board.tilemap = self.tilemap.copy()
        board._slidemap = self._slidemap.copy()
        board._mergemap = self._mergemap.copy()
        board._spawn_4_probability = self._spawn_4_probability
        return board

    def deterministic_copy(self):
        board = self.copy()
        board._random_state = self._random_state
        return board

    def get_tile(self, row, col):
        return self.tilemap[row][col]

    def move(self, direction: str):
        """Moves tiles in specified direction and spawns new tile if valid move"""
        self.move_tiles(direction)
        if self.valid_last_move: self.spawn_tile()

    def spawn_tile(self):
        clear_tiles = [(i,j) for i in range(self.size) for j in range (self.size) if self.tilemap[i][j] == 0]
        random.setstate(self._random_state)
        row, col = random.choice(clear_tiles)
        self.tilemap[row][col] = 2 if random.random() >= self._spawn_4_probability else 4
        self._random_state = random.getstate()
        return row, col

    def move_tiles(self, direction: str):
        """Moves tiles in specified direction: 'UP', 'DOWN', 'LEFT', 'RIGHT'"""
        self.valid_last_move = False
        if   direction.upper() == 'UP':     rotations = 3
        elif direction.upper() == 'LEFT':   rotations = 0
        elif direction.upper() == 'DOWN':   rotations = 1
        elif direction.upper() == 'RIGHT':  rotations = 2
        else: 
            print(f'{direction} not a valid direction')
            return
        
        self._slidemap = [[0 for i in range(self.size)] for j in range(self.size)]
        self._mergemap = [[0 for i in range(self.size)] for j in range(self.size)]

        # Rotate board to translate tiles left
        self.tilemap = self._rotate_CW(rotations, matrix=self.tilemap)
        self._slidemap = self._rotate_CW(rotations, matrix=self._slidemap)
        self._mergemap = self._rotate_CW(rotations, matrix=self._mergemap)

        # Translate and combine tiles to the left
        self._collapse_left()
        self.score += self._merge_left()
        self._collapse_left()

        # Rotate board back to original orientation
        self.tilemap = self._rotate_CCW(rotations, matrix=self.tilemap)
        self._slidemap = self._rotate_CCW(rotations, matrix=self._slidemap)
        self._mergemap = self._rotate_CCW(rotations, matrix=self._mergemap)

    def _rotate_CW(self, rotations, matrix: list):
        for _ in range(rotations):
            matrix = [[row[i] for row in matrix] for i in range(self.size)] # Transpose matrix along x = y
            matrix = [[row[j] for j in range(self.size-1,-1,-1)] for row in matrix] # Reverse rows of transpose
        return matrix

    def _rotate_CCW(self, rotations, matrix: list):
        for _ in range(rotations):
            matrix = [[matrix[i][j] for i in range(self.size-1,-1,-1)] for j in range(self.size-1,-1,-1)] # Transpose matrix along x = -y      
            matrix = [[row[j] for j in range(self.size-1,-1,-1)] for row in matrix] # Reverse rows of transpose
        return matrix

    def _collapse_left(self):
        """Collapses board to the left, removing any empty space between tiles"""
        for i in range(self.size):
            j = 0
            while j < self.size-1:
                empty = True
                if self.tilemap[i][j] == 0:             # Collapse row at index
                    for k in range(j, self.size-1, 1):
                        self.tilemap[i][k] = self.tilemap[i][k+1]
                        if self.tilemap[i][k] != 0:
                            self._slidemap[i][k] += self._slidemap[i][k+1] + 1
                            self._slidemap[i][k+1] = 0
                            self._mergemap[i][k] = self._mergemap[i][k+1]
                            self.valid_last_move = True
                            empty = False
                    self.tilemap[i][self.size-1] = 0

                if self.tilemap[i][j] != 0 or empty:    # Increment logic
                    j += 1
    
    def _merge_left(self):
        """Merges tiles to the left"""
        points = 0
        for i in range(self.size):
            for j in range(self.size-1):
                if self.tilemap[i][j] == self.tilemap[i][j+1] and self.tilemap[i][j] != 0:
                    self.tilemap[i][j], self.tilemap[i][j+1] = self.tilemap[i][j]*2, 0
                    self._slidemap[i][j] += self._slidemap[i][j+1] + 1
                    self._slidemap[i][j+1] = 0
                    self._mergemap[i][j] = 1
                    self.valid_last_move = True
                    points += self.tilemap[i][j]
        return points

    def pretty_print(self):
        print('    Board  \t    Slide Map  \t    Merge Map    ')
        for i in range(self.size):
            print(self.tilemap[i], '\t', self._slidemap[i], '\t', self._mergemap[i])   

if __name__ == '__main__':
    b = Board()
    b.spawn_tile()
    b.pretty_print()
    b.move('UP')
    b.pretty_print()