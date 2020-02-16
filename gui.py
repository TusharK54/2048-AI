
import tkinter as tk
from math import log
import numpy as np
from random import randint

from game import Move, GameState
from ai import BaseAI
from messaging import PubSub
from gui_colors import *

class View(tk.Frame, PubSub):

    def __init__(self, game: GameState, ai: BaseAI, master=None, fps: int=15):
        # 1. Initialize superclasses
        tk.Frame.__init__(self, master)
        PubSub.__init__(self)

        # 2a. Initialize game state game-dependent ui state
        self.game_state = game
        self.size = tk.IntVar()
        self.score = tk.IntVar()
        self.best = tk.IntVar()

        # 2b. Initialize ai state and ai-dependent ui state
        self.ai_state = ai
        self.ai_running = False
        self.next_state_vars = {move: (tk.StringVar(), tk.IntVar(), tk.IntVar()) for move in Move} # move : (valid var, evaluation var, score var)
        self.next_state_ui = {move: [] for move in Move} # move : tkinter widget that has a dynamic bg color

        # 3. Configure properties for the next step
        self.fps = 1000//fps
        self.canvas_map = {} # canvas : game
        self.initialize_fonts()

        # 4. Build UI
        width, height = 850, 650
        game_size = 520

        self.height = game_size + (height-game_size)

        control_panel = self.create_control_panel(game_size, height-game_size)
        game_panel = self.create_game_canvas(game_size)
        next_states_panel = self.create_states_panel(width-game_size, game_size)
        ai_state_panel = self.create_ai_panel(width-game_size, height-game_size)
        self.grid(sticky='nsew')

        control_panel.grid(sticky='nsew', row=0, column=0)
        game_panel.grid(sticky='nsew', row=1, column=0)
        next_states_panel.grid(sticky='nsew', row=1, column=1)
        ai_state_panel.grid(sticky='nsew', row=0, column=1)

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
        elif event == 'toggle ai':  # data contains bool ai running
            self.ai_running = data

        else:
            raise Exception

    def new_game_event(self):
        self.publish_event('restart', self.size.get())

    def step_ai_event(self):
        self.publish_event('step ai')

    def toggle_ai_event(self):
        if self.ai_running:
            self.publish_event('stop ai')
        else:
            self.publish_event('start ai')

    def launch_thread(self):
        """Launch the gui mainloop. NOTE: This launches a blocking thread!"""
        PubSub.launch_thread(self)
        self.mainloop()

    def initialize_fonts(self):
        self.tile_font    = ('Slope Opera', 48, 'bold')       # size sets '2048' title
        self.score_font       = ('Slope Opera', 20, 'bold')
        self.splash_font    = ('Hysterix', .8, 'bold')         # size acts at multiplier
        self.box_font = ('Hysterix', 12, '')
        self.button_font    = ('Hysterix', 12, '')
        
        self.state_move_font = ('Hysterix', 10, '')
        self.state_valid_font = ('Arial', 10, 'bold')
        self.state_score_font = ('Hysterix', 10, '')
        self.state_box_font = ('Slope Opera', 10, 'bold')


    def create_control_panel(self, width: int, height: int) -> tk.Frame:
        margin = height/35
        panel = tk.Frame(self, width=width, height=height, bg=INFO_BACKGROUND, padx=margin, pady=margin)
        panel.grid_propagate(0)

        # 2048 title
        title = tk.Label(panel, text='2048', font=self.tile_font, fg=TITLE, bg=INFO_BACKGROUND, padx=0, pady=0, bd=0)
        #title = tk.Canvas(panel, bg=INFO_BACKGROUND, bd=0)
        #text = title.create_text(15, -8, text='2048', fill=TITLE, font=self.('Arial', 50, 'bold'), anchor='nw')
        #bbox = title.bbox(text)  # get text bounding box
        #title.configure(width=bbox[2], height=bbox[3] - 30)

        # Score boxes
        score_box1 = tk.Frame(panel, bd=0, bg=SCORE_BOX)
        score_box2 = tk.Frame(panel, bd=0, bg=SCORE_BOX)

        score_label1 = tk.Label(score_box1, text='SCORE', width=7, bd=0, fg=SCORE_TITLE, bg=SCORE_BOX, font=self.box_font)
        score_label2 = tk.Label(score_box2, text='BEST', width=7, bd=0, fg=SCORE_TITLE, bg=SCORE_BOX, font=self.box_font)

        score_val1 = tk.Label(score_box1, textvariable=self.score, bd=0, fg=BUTTON_LABELS, bg=SCORE_BOX, font=self.score_font)
        score_val2 = tk.Label(score_box2,  textvariable=self.best, bd=0, fg=BUTTON_LABELS, bg=SCORE_BOX, font=self.score_font)

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
        button2.configure(command=self.toggle_ai_event)
        self.ai_toggle_button = button2

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

    def create_game_canvas(self, size: int) -> tk.Canvas:
        canvas = tk.Canvas(self, width=size, height=size, bg=TILE_GRID, bd=0, highlightthickness=0, cursor='crosshair')
        self.canvas_map[canvas] = None

        return canvas

    def create_states_panel(self, width: int, height: int) -> tk.Frame:
        margin=3
        panel = tk.Frame(self, width=width, height=height, bg=STATES_BACKGROUND, pady=margin/2)
        panel.grid_propagate(0)
        panel.rowconfigure(0, weight=1)
        panel.columnconfigure(0, weight=1)

        for i, move in enumerate(Move):
            state_panel = tk.Frame(panel, bg=STATES_BACKGROUND, pady=margin/2)
            _, eval_var, score_var = self.next_state_vars[move]

            # Data panel
            data_panel  = tk.Frame(state_panel, bg=STATES_BACKGROUND, padx=margin/2)
            move_box    = tk.Frame(data_panel)
            score_box   = tk.Frame(data_panel, bg=STATES_SCORE_BOX)
            eval_box    = tk.Frame(data_panel, bg=STATES_SCORE_BOX)

            move_box.grid(sticky='nsew')
            score_box.grid(sticky='nsew', pady=margin/2)
            eval_box.grid(sticky='nsew')

            data_panel.columnconfigure(0, weight=1)
            data_panel.rowconfigure(1, weight=1)
            data_panel.rowconfigure(2, weight=1)

            # Move box
            move_label  = tk.Label(move_box, text=move.name, font=self.state_move_font)
            move_label.grid(sticky='nsw', row=0, column=0)
            move_box.columnconfigure(0, weight=1)
            move_box.columnconfigure(1, weight=1)

            # Score box
            score_text  = tk.Label(score_box, bg=STATES_SCORE_BOX, fg=STATES_SCORE_BOX_TEXT, font=self.state_score_font, text='Game Score')
            score_label = tk.Label(score_box, bg=STATES_SCORE_BOX, fg=STATES_SCORE_BOX_VALUE, font=self.state_box_font,textvariable=score_var)
            score_text.grid(sticky='nsw', row=0)
            score_label.grid(sticky='nse', row=1)
            score_box.columnconfigure(0, weight=1)

            # Evaluation box
            eval_text   = tk.Label(eval_box, bg=STATES_SCORE_BOX, fg=STATES_SCORE_BOX_TEXT, font=self.state_score_font, text='AI Score')
            eval_label  = tk.Label(eval_box, bg=STATES_SCORE_BOX, fg=STATES_SCORE_BOX_VALUE, font=self.state_box_font, textvariable=eval_var)
            eval_text.grid(sticky='nsw', row=0)
            eval_label.grid(sticky='nse', row=1)
            eval_box.columnconfigure(0, weight=1)

            # Canvas
            canvas_size = (height-7*margin)/4 # Determines height of state panel
            move_canvas = tk.Canvas(state_panel, width=canvas_size, height=canvas_size, bg=TILE_GRID, bd=0, highlightthickness=0, cursor='crosshair')
            self.canvas_map[move_canvas] = move

            # Putting it together
            data_panel.grid(sticky='nsew', row=i, column=0)
            move_canvas.grid(sticky='nsew', row=i, column=1, padx=margin/2)

            state_panel.grid(sticky='nsew', row=i, padx=margin/2)
            state_panel.columnconfigure(0, weight=1)

            # Configure dynamic background color manager
            self.next_state_ui[move] = [score_box, score_text, score_label, eval_box, eval_text, eval_label]
            #self.next_state_ui[move] = [move_box, move_label]
        
        return panel

    def create_ai_panel(self, width: int, height: int) -> tk.Frame:
        panel = tk.Frame(self, width=width, height=height, bg=AI_BACKGROUND)

        return panel

    def animate(self):
        """Continually update the UI with the most recent state."""
        # Update control panel variables
        self.size.set(self.game_state.get_size())
        self.score.set(self.game_state.get_score())
        self.best.set(max(self.score.get(), self.best.get()))

        # Update control panel buttons
        if self.ai_running:
            self.ai_toggle_button.configure(bg=ENABLED_STANDARD_BUTTON, text='Disable AI')
        else:
            self.ai_toggle_button.configure(bg=DEFAULT_STANDARD_BUTTON, text='Enable AI')

        # Update ai panel variables and ui
        for move in Move:
            # Update variables
            valid_var, evaluation_var, score_var = self.next_state_vars[move]
            validity_str = 'valid' if self.game_state.valid_move(move) else 'invalid'
            valid_var.set(validity_str)
            evaluation_var.set(self.ai_state.evaluate_move(move))
            score_var.set(self.game_state.next_state(move).get_score())
            # Update ui
            for widget in self.next_state_ui[move]:
                if valid_var.get().lower() == 'valid':
                    widget.configure(bg=VALID_STATE_BOX)
                elif valid_var.get().lower() == 'invalid':
                    widget.configure(bg=INVALID_STATE_BOX)

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

                number_font = (self.tile_font[0], int(text_size), self.tile_font[2])
                canvas.create_rectangle(x0, y0, x1, y1, width=0, fill=tile_color)
                canvas.create_text((x0+x1)/2, (y0+y1)/2, text=tile, fill=text_color, justify='center', font=number_font)

        if game.game_over():
            title_font = (self.splash_font[0], int(canvas_size/9*(self.splash_font[1])), self.splash_font[2])
            canvas.create_rectangle(0, 0, canvas_size, canvas_size, width=0, fill=GAME_OVER_STIPPLE, stipple='gray50')
            canvas.create_text(canvas_size/2, canvas_size/2, fill=TITLE, font=title_font, text='GAME OVER')

if __name__ == '__main__':
    from ai import DummyAI
    root = tk.Tk()
    game = GameState()
    ai = DummyAI(game)

    view = View(game, ai, root)
    view.mainloop()