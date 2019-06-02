import tkinter as tk
from json import load
from time import sleep

from game import Board
import constants

class Window:

    tile_colorfile = 'colorinfo.txt'
    with open(tile_colorfile) as f:
        tile_colors = load(f)

    def __init__(self, size=500, pad=20, windowName='2048 Game', board=None, human=True):
        self.size = size
        self.pad = pad
        self.human = True
        self.best = 0
        self.board = Board() if board is None else board

        # Create canvas and info panel
        self.root = tk.Tk(className=windowName)
        self.info_panel = tk.Frame(self.root, height=150, bg='#faf8ef')
        self.info_panel.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas = tk.Canvas(self.root, width=size+pad, height=size+pad, bg='#938578', bd=0, highlightthickness=0)
        self.canvas.pack()

        # Create info panel widgets
        self.title = tk.Text(self.info_panel, height=1, width=4, font=('Arial', 60, 'bold'), relief=tk.FLAT, pady=0, bd=0, fg='#453C33', bg='#faf8ef')
        self.title.insert(tk.INSERT, '2048')
        self.score_var = tk.StringVar()
        self.score_box = tk.Frame(self.info_panel, bd=0, bg=constants.BACKGROUND)
        self.score_label = tk.Label(self.score_box, text='SCORE', width=7, bd=0, fg='#eee4da', bg=constants.BACKGROUND, font=('Arial', 12, 'bold'))
        self.score_value = tk.Label(self.score_box, textvariable=self.score_var, bd=0, fg='#f9f6f2', bg=constants.BACKGROUND, font=('Arial', 20, 'bold'))
        self.score_label.pack()
        self.score_value.pack()
        self.best_var = tk.StringVar()
        self.best_box = tk.Frame(self.info_panel, bd=0, bg=constants.BACKGROUND)
        self.best_label = tk.Label(self.best_box, text='BEST', width=7, bd=0, fg='#eee4da', bg=constants.BACKGROUND, font=('Arial', 12, 'bold'))
        self.best_value = tk.Label(self.best_box, textvariable=self.best_var, bd=0, fg='#f9f6f2', bg=constants.BACKGROUND, font=('Arial', 20, 'bold'))
        self.best_label.pack()
        self.best_value.pack()

        def new_human_game():
            self.human = True
            self.new_game()
        self.button1 = tk.Button(self.info_panel, text='New Game', width=8, command=new_human_game, bg='#8f7a66', fg='#f9f6f2', font=('Arial', 10, 'bold'), relief=tk.FLAT)
        
        def new_AI_game():
            self.human = False
            self.new_game()
        self.button2 = tk.Button(self.info_panel, text='Set Size', width=8, command=new_AI_game, bg='#8f7a66', fg='#f9f6f2', font=('Arial', 10, 'bold'), relief=tk.FLAT)
        
        # Pack the info panel widgets
        pad = 3
        self.title.grid(rowspan=2, sticky='w', padx=15)
        self.score_box.grid(row=0, column=1, padx=0, pady=pad, sticky='nsew')
        self.best_box.grid(row=0, column=2, padx=pad*2, pady=pad, sticky='nsew')
        self.button1.grid(row=1, column=1, padx=0, pady=pad, sticky='nsew')
        self.button2.grid(row=1, column=2, padx=pad*2, pady=pad, sticky='nsew')
        self.info_panel.grid_columnconfigure(1, weight=1)
        self.info_panel.grid_columnconfigure(2, weight=1)

        # Bind keyboard inputs to functions
        self.root.bind('<Up>', self.keypress_up)
        self.root.bind('<Down>', self.keypress_down)
        self.root.bind('<Left>', self.keypress_left)
        self.root.bind('<Right>', self.keypress_right)

        self.new_game()

    def new_game(self):
        self.board.reset()
        self.draw_board()

    def move_board(self, direction):
        self.board.move(direction)
        if self.best < self.board.score: self.best = self.board.score
        self.draw_board()

    def draw_board(self):
        tile_size = self.size / self.board.size

        # Update info panel
        self.score_var.set(str(self.board.score))
        self.best_var.set(str(self.best))

        # Draw tiles on canvas
        self.canvas.delete("all")
        for i in range(self.board.size):
            for j in range(self.board.size):
                tile = self.board.get_tile(i,j)
                try:
                    color = Window.tile_colors[str(tile)]
                except KeyError:
                    color = Window.tile_colors['default']
                
                self.canvas.create_rectangle(j*tile_size+self.pad, i*tile_size+self.pad, (j+1)*tile_size, (i+1)*tile_size, fill=color['tile'], width=0)
                self.canvas.create_text(j*tile_size+(tile_size+self.pad)/2, i*tile_size+(tile_size+self.pad)/2, text=tile, justify='center', width=tile_size, font=('Helvetica Neue', 42, 'bold'), fill=color['text'])
    
    def keypress_up(self, event):
        if self.human:
            self.move_board('UP')

    def keypress_down(self, event):
        if self.human: 
            self.move_board('DOWN')

    def keypress_left(self, event):
        if self.human: 
            self.move_board('LEFT')

    def keypress_right(self, event):
        if self.human: 
            self.move_board('RIGHT')

if __name__ == '__main__':

    board = Board()
    game = Window()

    board.spawn_tile()
    board.spawn_tile()

    game.draw_board()
    game.root.mainloop()