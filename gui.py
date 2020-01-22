
import tkinter as tk
from math import log
import numpy as np
from random import randint

from game import Move, GameState
from ai import Base
from pub_sub import Publisher
from gui_colors import *

class View(tk.Frame, Publisher):

    def __init__(self, game: GameState, ai: Base, master=None, fps: int=15):
        # 1. Initialize superclasses
        tk.Frame.__init__(self, master)
        Publisher.__init__(self)

        # 2a. Initialize game state
        self.game_state = game
        self.size = tk.IntVar()
        self.score = tk.IntVar()
        self.best = tk.IntVar()

        # 2b. Initialize AI state
        self.ai_state = ai
        self.next_game_states = {} # move : (valid var, evaluation var, score var)
        for move in Move:
            self.next_game_states[move] = (tk.StringVar(), tk.IntVar(), tk.IntVar())

        # 3. Configure properties for the next step
        self.fps = 1000//fps
        self.canvas_map = {} # canvas : game
        self.initialize_fonts()

        # 4. Build UI
        control_panel_height = 130
        game_panel_size = 520
        ai_panel_width = 330

        self.height = game_panel_size + control_panel_height
        self.width = game_panel_size + ai_panel_width

        control_panel = self.create_control_panel(control_panel_height)
        game_panel = self.create_game_canvas(self.height-control_panel_height)
        ai_panel = self.create_ai_panel(self.width-(self.height-control_panel_height))
        self.grid(sticky='nsew')

        control_panel.grid(sticky='nsew', row=0, column=0)
        game_panel.grid(sticky='nsew', row=1, column=0)
        ai_panel.grid(sticky='nsew', row=0, column=1, rowspan=2)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        master.resizable(False, False)

        # 5. Launch self refresher
        self.animate()

    def handle_event(self, event, data):
        if event == 'new game':     # data contains new game state
            self.game_state = data
        elif event == 'new ai':     # data contains new ai state
            self.ai_state = data

        else:
            raise Exception

    def ai_toggle_event(self):
        pass

    def new_game_event(self):
        self.publish_event('restart', self.size.get())

    def launch_thread(self):
        """Launch the gui mainloop. NOTE: This launches a blocking thread!"""
        Publisher.launch_thread(self)
        self.mainloop()

    def initialize_fonts(self):
        self.number_font    = ('Slope Opera', 48, 'bold')       # size sets '2048' title
        self.box_font       = ('Slope Opera', 20, 'bold')
        self.splash_font     = ('Hysterix', .8, 'bold')         # size acts at multiplier
        self.box_title_font = ('Hysterix', 12, '')
        self.button_font    = ('Hysterix', 12, '')

    def create_control_panel(self, height: int):
        margin = height/35
        panel = tk.Frame(self, height=height, bg=INFO_BACKGROUND, padx=margin, pady=margin)
        panel.grid_propagate(0)

        # 2048 title
        title = tk.Label(panel, text='2048', font=self.number_font, fg=TITLE, bg=INFO_BACKGROUND, padx=0, pady=0, bd=0)
        #title = tk.Canvas(panel, bg=INFO_BACKGROUND, bd=0)
        #text = title.create_text(15, -8, text='2048', fill=TITLE, font=self.('Arial', 50, 'bold'), anchor='nw')
        #bbox = title.bbox(text)  # get text bounding box
        #title.configure(width=bbox[2], height=bbox[3] - 30)

        # Score boxes
        score_box1 = tk.Frame(panel, bd=0, bg=SCORE_BOX)
        score_box2 = tk.Frame(panel, bd=0, bg=SCORE_BOX)

        score_label1 = tk.Label(score_box1, text='SCORE', width=7, bd=0, fg=SCORE_TITLE, bg=SCORE_BOX, font=self.box_title_font)
        score_label2 = tk.Label(score_box2, text='BEST', width=7, bd=0, fg=SCORE_TITLE, bg=SCORE_BOX, font=self.box_title_font)

        score_val1 = tk.Label(score_box1, textvariable=self.score, bd=0, fg=BUTTON_LABELS, bg=SCORE_BOX, font=self.box_font)
        score_val2 = tk.Label(score_box2,  textvariable=self.best, bd=0, fg=BUTTON_LABELS, bg=SCORE_BOX, font=self.box_font)

        score_label1.grid(sticky='nsew')
        score_label2.grid(sticky='nsew')
        score_val1.grid(sticky='nsew')
        score_val2.grid(sticky='nsew')

        score_box1.columnconfigure(0, weight=1)
        score_box2.columnconfigure(0, weight=1)
        score_box1.rowconfigure(0, weight=1)
        score_box1.rowconfigure(1, weight=1)
        score_box2.rowconfigure(0, weight=1)
        score_box2.rowconfigure(1, weight=1)

        # Size buttons
        size_buttons = tk.Frame(panel)
        for i in range(3, 7):
            size_button = tk.Radiobutton(size_buttons, variable=self.size, value=i, text=i, indicatoron=0, width=2, bg=DEFAULT_SIZE_BUTTON, fg=BUTTON_LABELS, activeforeground=BUTTON_LABELS, activebackground=ENABLED_SIZE_BUTTON, selectcolor=ENABLED_SIZE_BUTTON, font=self.button_font, bd=0, relief=tk.FLAT)
            size_button.grid(row=0, column=i, sticky='nsew')
            size_buttons.columnconfigure(i, weight=1)
        size_buttons.rowconfigure(0, weight=1)

        # Standard buttons
        button1 = tk.Button(panel, width=8, bd=0, font=self.button_font, relief=tk.FLAT, fg=BUTTON_LABELS, bg=DEFAULT_STANDARD_BUTTON, disabledforeground=BUTTON_LABELS, activeforeground=BUTTON_LABELS, activebackground=PRESSED_STANDARD_BUTTON, text='Restart')
        button2 = tk.Button(panel, width=8, bd=0, font=self.button_font, relief=tk.FLAT, fg=BUTTON_LABELS, bg=DEFAULT_STANDARD_BUTTON, disabledforeground=BUTTON_LABELS, activeforeground=BUTTON_LABELS, activebackground=PRESSED_STANDARD_BUTTON, text='Enable AI')
        self.ai_button = button2

        # Configure button events
        for button in size_buttons.winfo_children():
            button.configure(command=self.new_game_event)
        button1.configure(command=self.new_game_event)
        button2.configure(command=self.ai_toggle_event)

        # Position widgets into place
        title.grid(row=0, column=0, sticky='nsew')
        score_box1.grid(row=0, column=1, sticky='nsew', padx=margin, pady=margin)
        score_box2.grid(row=0, column=2, sticky='nsew', padx=margin, pady=margin)
        size_buttons.grid(row=1, column=0, sticky='nsew', padx=margin, pady=margin)
        button1.grid(row=1, column=1, sticky='nsew', padx=margin, pady=margin)
        button2.grid(row=1, column=2, sticky='nsew', padx=margin, pady=margin)

        panel.rowconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)
        panel.columnconfigure(0, weight=1)
        panel.columnconfigure(1, weight=5)
        panel.columnconfigure(2, weight=5)

        return panel

    def create_game_canvas(self, size: int):
        canvas = tk.Canvas(self, width=size, height=size, bg=TILE_GRID, bd=0, highlightthickness=0, cursor='crosshair')
        self.canvas_map[canvas] = None

        return canvas

    def create_ai_panel(self, width: int):
        panel = tk.Frame(self, width=width, bg='blue')
        panel.grid_propagate(0)
        panel.rowconfigure(0, weight=1)
        panel.rowconfigure(1, weight=0)

        # Info panel
        info_panel = tk.Frame(panel, width=width, bg='green')
        info_panel.grid(sticky='nsew')


        #TODO: move asthetics
        pane_border = width/50
        grid_color = 'black'

        # Next states panel
        states_container = tk.Frame(panel, width=width, bg=grid_color, pady=pane_border/2, padx=pane_border)
        states_container.grid(sticky='nsew')
        states_container.columnconfigure(0, weight=1)

        for i, move in enumerate(Move):
            state_panel = tk.Frame(states_container, bg=grid_color, pady=pane_border/2)
            valid_var, eval_var, score_var = self.next_game_states[move]

            # Data panel
            data_panel  = tk.Frame(state_panel, bg='red')
            move_label  = tk.Label(data_panel, text=move.name, font=('Arial', 10, 'bold'))
            eval_text   = tk.Label(data_panel, text='Evaluation')
            score_text  = tk.Label(data_panel, text='Score')
            valid_label = tk.Label(data_panel, textvariable=valid_var, font=('Arial', 10, 'bold'))
            eval_label  = tk.Label(data_panel, textvariable=eval_var)
            score_label = tk.Label(data_panel, textvariable=score_var)

            move_label.grid(sticky='nsw',  row=0, column=0)
            valid_label.grid(sticky='nse', row=0, column=1)
            eval_text.grid(sticky='nsw',   row=1, column=0)
            eval_label.grid(sticky='nse',  row=1, column=1)
            score_text.grid(sticky='nsw',  row=2, column=0)
            score_label.grid(sticky='nse', row=2, column=1)

            data_panel.columnconfigure(0, weight=0)
            data_panel.columnconfigure(0, weight=1)

            # Canvas
            move_canvas = tk.Canvas(state_panel, width=self.height/5, height=self.height/5, bg=TILE_GRID, bd=0, highlightthickness=0, cursor='crosshair')
            self.canvas_map[move_canvas] = move

            # Putting it together
            data_panel.grid(sticky='nsew', row=i, column=0)
            move_canvas.grid(sticky='nsew', row=i, column=1)

            state_panel.grid(sticky='nsew', row=i)
            state_panel.columnconfigure(0, weight=1)
        
        return panel

    def animate(self):
        """Continually update the UI with the most recent state."""
        # Update control panel variables
        self.size.set(self.game_state.get_size())
        self.score.set(self.game_state.get_score())
        self.best.set(max(self.score.get(), self.best.get()))

        # Update ai panel variables
        for move in Move:
            valid_var, evaluation_var, score_var = self.next_game_states[move]
            validity_str = 'valid' if self.game_state.valid_move(move) else 'invalid'
            valid_var.set(validity_str)
            evaluation_var.set(self.ai_state.evaluate_move(move))
            score_var.set(self.game_state.next_state(move).get_score())

        # Update canvases
        for canvas in self.canvas_map:
            move = self.canvas_map[canvas]
            game = self.game_state if move is None else self.game_state.next_state(move)
            self.draw_canvas(canvas, game)

        # Call this function again after a set time
        self.after(self.fps, self.animate)

    def draw_canvas(self, canvas: tk.Canvas, game: GameState):
        """Draws `game` onto `canvas`."""
        grid = game.get_matrix()

        grid_size = len(grid)
        canvas_size = canvas.winfo_width()
        margin = canvas_size//grid_size//10
        tile_size = (canvas_size - margin * (grid_size + 1)) / grid_size

        canvas.delete("all")
        for x in range(grid_size):
            for y in range(grid_size):
                tile = grid[y][x]

                try:
                    tile_color = TILES[str(tile)]['tile']
                    text_color = TILES[str(tile)]['text']
                except KeyError:
                    tile_color = TILES['default']['tile']
                    text_color = TILES['default']['text']

                x0, x1 = (x+1)*margin + x*tile_size, (x+1)*margin + (x+1)*tile_size
                y0, y1 = (y+1)*margin + y*tile_size, (y+1)*margin + (y+1)*tile_size

                text_size = tile_size/3 if (tile == 0 or log(tile, 10) < 2) else tile_size/int(log(tile, 10)+1)

                number_font = (self.number_font[0], int(text_size), self.number_font[2])
                canvas.create_rectangle(x0, y0, x1, y1, width=0, fill=tile_color)
                canvas.create_text((x0+x1)/2, (y0+y1)/2, text=tile, fill=text_color, justify='center', font=number_font)

        if game.game_over():
            title_font = (self.splash_font[0], int(canvas_size/9*(self.splash_font[1])), self.splash_font[2])
            canvas.create_rectangle(0, 0, canvas_size, canvas_size, width=0, fill=GAME_OVER_STIPPLE, stipple='gray50')
            canvas.create_text(canvas_size/2, canvas_size/2, fill=TITLE, font=title_font, text='GAME OVER')

if __name__ == '__main__':
    from ai import Dummy
    root = tk.Tk()
    game = GameState()
    ai = Dummy(game)

    view = View(game, ai, root)
    view.mainloop()