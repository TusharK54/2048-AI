import tkinter as tk
from json import load
from math import log

from board import Game
from tree import MoveTree
import color_constants as color

class Window:

    def __init__(self, size=500):
        self.size = size
        self.human = True
        self.best = {3:0, 4:0, 5:0, 6:0}
        self.board = Game()
        self.ai_lookahead = 4               # Number of moves the ai looks ahead (values >5 cause slow performance)
        self.ai_speed = self.ai_lookahead   # Time between ai moves in milliseconds
        
        # Create canvas and info panel
        self.root = tk.Tk(className='2048 AI')
        self.root.resizable(False, False)
        self.info_panel = tk.Frame(self.root, height=150, bg=color.INFO_BACKGROUND)
        self.info_panel.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas = tk.Canvas(self.root, width=size, height=size, bg=color.TILE_GRID, bd=0, highlightthickness=0)
        self.canvas.pack()

        # Create info panel widgets
        self.title = tk.Text(self.info_panel, height=1, width=4, font=('Arial', 50, 'bold'), relief=tk.FLAT, fg=color.TITLE, bg=color.INFO_BACKGROUND, pady=-8)
        self.title.insert(tk.INSERT, '2048')
        self.title.config(state=tk.DISABLED)
        self.score_var = tk.StringVar()
        self.score_box = tk.Frame(self.info_panel, bd=0, bg=color.SCORE_BOX)
        self.score_label = tk.Label(self.score_box, text='SCORE', width=7, bd=0, fg=color.SCORE_TITLE, bg=color.SCORE_BOX, font=('Arial', 12, 'bold'))
        self.BUTTON_LABELS = tk.Label(self.score_box, textvariable=self.score_var, bd=0, fg=color.BUTTON_LABELS, bg=color.SCORE_BOX, font=('Arial', 20, 'bold'))
        self.score_label.pack(anchor=tk.S, expand=True)
        self.BUTTON_LABELS.pack(anchor=tk.N, expand=True)
        self.best_var = tk.StringVar()
        self.best_box = tk.Frame(self.info_panel, bd=0, bg=color.SCORE_BOX)
        self.best_label = tk.Label(self.best_box, text='BEST', width=7, bd=0, fg=color.SCORE_TITLE, bg=color.SCORE_BOX, font=('Arial', 12, 'bold'))
        self.best_value = tk.Label(self.best_box, textvariable=self.best_var, bd=0, fg=color.BUTTON_LABELS, bg=color.SCORE_BOX, font=('Arial', 20, 'bold'))
        self.best_label.pack(anchor=tk.S, expand=True)
        self.best_value.pack(anchor=tk.N, expand=True)
        
        self.size_buttons = []
        def change_size(new_size):
            if self.board.size == new_size or not self.human: return
            self.board = Game(size=new_size)
            self._new_game()
            for button in self.size_buttons:
                if button['text'] == str(new_size):
                    button['bg'] = color.ENABLED_SIZE_BUTTON
                else:
                    button['bg'] = color.DEFAULT_SIZE_BUTTON

        self.size_buttons_frame = tk.Frame(self.info_panel, relief=tk.FLAT)
        self.size_button_3 = tk.Button(self.size_buttons_frame, width=2, text='3', command=lambda:change_size(3), bg=color.DEFAULT_SIZE_BUTTON, fg=color.BUTTON_LABELS, disabledforeground=color.BUTTON_LABELS, font=('Arial', 10, 'bold'), relief=tk.FLAT)
        self.size_button_4 = tk.Button(self.size_buttons_frame, width=2, text='4', command=lambda:change_size(4), bg=color.ENABLED_SIZE_BUTTON, fg=color.BUTTON_LABELS, disabledforeground=color.BUTTON_LABELS, font=('Arial', 10, 'bold'), relief=tk.FLAT)
        self.size_button_5 = tk.Button(self.size_buttons_frame, width=2, text='5', command=lambda:change_size(5), bg=color.DEFAULT_SIZE_BUTTON, fg=color.BUTTON_LABELS, disabledforeground=color.BUTTON_LABELS, font=('Arial', 10, 'bold'), relief=tk.FLAT)
        self.size_button_6 = tk.Button(self.size_buttons_frame, width=2, text='6', command=lambda:change_size(6), bg=color.DEFAULT_SIZE_BUTTON, fg=color.BUTTON_LABELS, disabledforeground=color.BUTTON_LABELS, font=('Arial', 10, 'bold'), relief=tk.FLAT)
        self.size_button_3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.size_button_4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.size_button_5.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.size_button_6.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.size_buttons.append(self.size_button_3)
        self.size_buttons.append(self.size_button_4)
        self.size_buttons.append(self.size_button_5)
        self.size_buttons.append(self.size_button_6)

        self.button1 = tk.Button(self.info_panel, text='New Game', width=8, command=self._new_game, bg=color.DEFAULT_STANDARD_BUTTON, fg=color.BUTTON_LABELS, disabledforeground=color.BUTTON_LABELS, font=('Arial', 10, 'bold'), relief=tk.FLAT)
        self.player_button_var = tk.StringVar()
        self.player_button_var.set('Enable AI')
        self.button2 = tk.Button(self.info_panel, textvariable=self.player_button_var, width=8, command=self._toggle_ai, bg=color.DEFAULT_STANDARD_BUTTON, fg=color.BUTTON_LABELS, disabledforeground=color.BUTTON_LABELS, font=('Arial', 10, 'bold'), relief=tk.FLAT)
        
        # Pack the info panel widgets
        pad = 3
        self.title.grid(rowspan=1, sticky='w', padx=15)
        self.score_box.grid(row=0, column=1, padx=0, pady=pad, sticky='nsew')
        self.best_box.grid(row=0, column=2, padx=pad*2, pady=pad, sticky='nsew')
        self.size_buttons_frame.grid(row=2, column=0, padx=pad*2, pady=pad, sticky='nsew')
        self.button1.grid(row=2, column=1, padx=0, pady=pad, sticky='nsew')
        self.button2.grid(row=2, column=2, padx=pad*2, pady=pad, sticky='nsew')
        self.info_panel.grid_columnconfigure(1, weight=1)
        self.info_panel.grid_columnconfigure(2, weight=1)

        # Bind keyboard inputs to functions
        self.root.bind('<Up>', self._keypress_up)
        self.root.bind('<Down>', self._keypress_down)
        self.root.bind('<Left>', self._keypress_left)
        self.root.bind('<Right>', self._keypress_right)

        self._new_game()
        self.root.mainloop()

    def _new_game(self):
        if not self.human: return
        self.gameover = False
        self.button2['state'] = tk.NORMAL
        if hasattr(self, 'return_bind'):
            self.root.unbind('<Return>', self.return_bind)
        self.return_bind = self.root.bind('<Return>', self._toggle_ai)

        self.board.reset()
        self.ai = MoveTree(self.board, iterations=self.ai_lookahead)
        self._update_ui()

    def _game_over(self):
        self.gameover = True
        self.button2['state'] = tk.DISABLED
        self.root.unbind('<Return>', self.return_bind)
        self.return_bind = self.root.bind('<Return>', lambda event: self._new_game())
        if not self.human:
            self._toggle_ai()

    def _move_board(self, direction):
        self.board.move(direction)
        if self.best[self.board.size] < self.board.score: 
            self.best[self.board.size] = self.board.score
        if not self.board._remaining_moves():
            self._game_over()
        self._update_ui()

    def _update_ui(self):
        tile_size = self.size/self.board.size
        tile_border = tile_size/10

        # Update info panel
        self.score_var.set(str(self.board.score))
        self.best_var.set(str(self.best[self.board.size]))

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

        if self.gameover:
            self.canvas.create_rectangle(0, 0, self.size, self.size, width=0, fill=color.GAME_OVER_STIPPLE, stipple='gray50')
            self.canvas.create_text(self.size/2, self.size/2-25, text='Game Over', font=('Arial', 50, 'bold'), fill=color.TITLE)
            self.canvas.create_text(self.size/2, self.size/2+25, text='Press [ENTER] to play again', font=('Helvetica Neue', 15, 'bold'), fill=color.TITLE)

    def _ai_play(self):
        move = self.ai.get_best_move()
        self._move_board(move)
        self.ai.update_board(move)
        if not self.human:
            self.root.after(self.ai_speed, self._ai_play)

    def _toggle_ai(self, event=None):
        self.human = not self.human
        if self.human:
            self.button2.configure(bg=color.DEFAULT_STANDARD_BUTTON)
            self.button1['state'] = tk.NORMAL
            for button in self.size_buttons:
                button['state'] = tk.NORMAL
            self.player_button_var.set('Enable AI')
        else:
            self.button2.configure(bg=color.ENABLED_STANDARD_BUTTON)
            self.button1['state'] = tk.DISABLED
            for button in self.size_buttons:
                button['state'] = tk.DISABLED
            self.player_button_var.set('Disable AI')
            self.ai = MoveTree(self.board, iterations=self.ai_lookahead)
            self._ai_play()

    def _keypress_up(self, event):
        if self.human:
            self._move_board(Game.UP)

    def _keypress_down(self, event):
        if self.human: 
            self._move_board(Game.DOWN)

    def _keypress_left(self, event):
        if self.human: 
            self._move_board(Game.LEFT)

    def _keypress_right(self, event):
        if self.human: 
            self._move_board(Game.RIGHT)

if __name__ == '__main__':

    game = Window()