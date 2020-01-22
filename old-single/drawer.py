"""This module simply draws a provided game state to the screen. It should not be imported."""

import tkinter as tk
from json import load
from math import log

from board import GameState
from node import BoardNode
import color_constants as color

class Window:

    def __init__(self, size=500):
        self.size = size
        self.board = GameState()
        self.board.tilemap = [[4,   8,   32, 2],
                              [2,   128, 32,  2],
                              [2,   64,   0,  0],
                              [0,   0,   0,  0]]
        self.board.score = 1000
        self.board_tree = [BoardNode(self.board)]
        
        # Create canvas and info panel
        self.root = tk.Tk(className='2048 AI')
        self.canvas = tk.Canvas(self.root, width=size+12.5, height=size+12.5, bg=color.TILE_GRID, bd=0, highlightthickness=0)
        self.canvas.pack()
        
        self.root.bind('<Return>', self._update_board)
        self._update_ui()
        self.root.mainloop()

    def _update_ui(self):
        tile_size = self.size/self.board.size
        tile_border = tile_size/10

        # Draw tiles on canvas
        self.canvas.delete("all")
        for i in range(self.board.size):
            for j in range(self.board.size):
                tile = self.board.get_tile(i,j)
                if tile == 0 or log(tile, 10) < 2:
                    tile_text_size = tile_size/3
                else:
                    tile_text_size = tile_size/int(log(tile, 10)+1)

                try:
                    tile_color = color.TILES[str(tile)]
                except KeyError:
                    tile_color = color.TILES['default']
                
                self.canvas.create_rectangle(j*tile_size+tile_border, i*tile_size+tile_border, (j+1)*tile_size, (i+1)*tile_size, fill=tile_color['tile'], width=0)
                self.canvas.create_text(j*tile_size+(tile_size+tile_border)/2, i*tile_size+(tile_size+tile_border)/2, text=tile, justify='center', width=tile_size, font=('Helvetica Neue', int(tile_text_size), 'bold'), fill=tile_color['text'])

    def _update_board(self, event=None):
        node = self.board_tree.pop(0)
        self.board_tree += node.generate_children()
        self.board = self.board_tree[0].board
        print(f'depth: {self.board_tree[0].depth}, \tmove: {self.board_tree[0].move}, \tscore: {self.board_tree[0].get_evaluation_score()}')
        self._update_ui()

if __name__ == '__main__':

    game = Window()