
import tkinter as tk
from math import log
import numpy as np

from game import Move, GameState
from pub_sub import Publisher
from gui_colors import *

class ViewModel():

    def __init__(self, game: GameState=None):
        self.game_state = game
        self.size = tk.IntVar()
        self.score = tk.IntVar()
        self.best = tk.IntVar()
        self.ai_enabled = False

        self.update_vars()

        self.next_states = {} # Caches next states so they don't have to be recomputed

    def update_state(self, game: GameState):
        self.game_state = game
        self.next_states = {}
        self.update_vars()

    def update_vars(self):
        self.size.set(self.game_state.get_size())
        self.score.set(self.game_state.get_score())
        if self.score.get() > self.best.get():
            self.best.set(self.score.get())
    
    def set_ai_enabled(self, new: bool):
        self.ai_enabled = new

    def get_size_var(self) -> tk.IntVar:
        """Return a `tk.IntVar` object containing the grid size."""
        return self.size

    def get_score_var(self) -> tk.IntVar:
        """Return a `tk.IntVar` object containing the current game score."""
        return self.score

    def get_best_var(self) -> tk.IntVar:
        """Return a `tk.IntVar` object containing the best game score."""
        return self.best

    def get_grid(self) -> np.ndarray:
        """Return a matrix of the game tiles."""
        return self.game_state.get_matrix()

    def get_game_over(self) -> bool:
        """Return `True` only if the game is over."""
        return self.game_state.game_over()

    def get_ai_enabled(self) -> bool:
        """Return `True` only if an AI is enabled."""
        return self.ai_enabled

    def get_next_state(self, move: Move):
        if self.next_states.get(move) is None:
            self.next_states[move] = ViewModel(self.game_state.next_state(move))
        return self.next_states[move]

class View(tk.Frame, Publisher):

    def __init__(self, game: GameState, master=None, fps: int=15):
        # 1. Initialize superclasses
        tk.Frame.__init__(self, master)
        Publisher.__init__(self)

        # 2. Configure properties for the next step
        self.model = ViewModel(game)
        self.fps = 1000//fps
        self.canvas_map = {}    # canvas : model
        self.initialize_fonts()

        # 3. Build UI and launch canvas animations
        control_panel = self.create_control_panel(150)
        game_panel = self.create_game_canvas(500)
        ai_panel = self.create_ai_panel(300)
        self.grid(sticky='nsew')

        control_panel.grid(sticky='nsew', row=0, column=0)
        game_panel.grid(sticky='nsew', row=1, column=0)
        ai_panel.grid(sticky='nsew', row=0, column=1, rowspan=2)

    def handle_event(self, event, data):
        if event == 'update game':
            self.model.update_state(data)
        elif event == 'enable ai':
            self.model.set_ai_enabled(True)
            self.ai_button.configure(bg=ENABLED_STANDARD_BUTTON, text='Disable AI')
        elif event == 'disable ai':
            self.model.set_ai_enabled(False)
            self.ai_button.configure(bg=DEFAULT_STANDARD_BUTTON, text='Enable AI')
        
        else:
            raise Exception

    def ai_toggle_event(self):
        if self.model.get_ai_enabled():
            self.publish_event('view disable ai')
        else:
            self.publish_event('view enable ai')
        self.model.set_ai_enabled(not self.model.get_ai_enabled())

    def new_game_event(self):
        self.publish_event('restart', self.model.get_size_var().get())

    def launch_thread(self):
        """NOTE: This launches a blocking thread!"""
        Publisher.launch_thread(self)
        self.mainloop()

    def initialize_fonts(self):
        self.number_font    = ('Slope Opera', 45, 'bold')       # size sets '2048' title
        self.box_font       = ('Slope Opera', 20, 'bold')
        self.title_font     = ('Hysterix', .8, 'bold')          # size acts at multiplier
        
        self.box_title_font = ('Hysterix', 12, '')
        self.button_font    = ('Hysterix', 10, '')

    def create_control_panel(self, height: int):
        margin = 3
        panel = tk.Frame(self, height=height, bg=INFO_BACKGROUND, padx=margin, pady=margin)

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

        score_val1 = tk.Label(score_box1, textvariable=self.model.get_score_var(), bd=0, fg=BUTTON_LABELS, bg=SCORE_BOX, font=self.box_font)
        score_val2 = tk.Label(score_box2,  textvariable=self.model.get_best_var(), bd=0, fg=BUTTON_LABELS, bg=SCORE_BOX, font=self.box_font)

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
            size_button = tk.Radiobutton(size_buttons, variable=self.model.get_size_var(), value=i, text=i, indicatoron=0, width=2, bg=DEFAULT_SIZE_BUTTON, fg=BUTTON_LABELS, activeforeground=BUTTON_LABELS, activebackground=ENABLED_SIZE_BUTTON, selectcolor=ENABLED_SIZE_BUTTON, font=self.button_font, bd=0, relief=tk.FLAT)
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
        self.animate_canvas(canvas)

        return canvas

    def create_ai_panel(self, width: int):
        panel = tk.Frame(self, width=width, bg='blue')
        panel.columnconfigure(0, weight=1)

        states_container = tk.Frame(panel, width=width)
        states_container.grid(sticky='sew')

        for i, move in enumerate(Move):
            model = self.model.get_next_state(move)
            score = model.get_score_var().get()

            move_panel = tk.Frame(states_container, width=width, bg='red', bd=2)
            move_panel.grid(sticky='nsew')

            states_container.columnconfigure(i, weight=1)
            move_panel.columnconfigure(0, weight=1)
            move_panel.columnconfigure(2, weight=0)
            
            title = tk.Label(move_panel, text=move.name, font=('Arial', 10, 'bold'))
            title.grid(sticky='nsew', row=0, column=0)
           
            move_label = tk.Label(move_panel, text=score)

            move_canvas = tk.Canvas(move_panel, width=width/3, height=width/3, bg=TILE_GRID, bd=0, highlightthickness=0, cursor='crosshair')
            move_canvas.grid(sticky='nsew', row=1, column=0)
            self.animate_canvas(move_canvas, move)
        
        return panel

    def draw_all_canvases(self):
        for canvas in self.canvas_map:
            model = self.model if self.canvas_map[canvas] is None else self.model.get_next_state(move)
            self.draw_canvas(canvas, model)

    def animate_canvas(self, canvas: tk.Canvas, move: Move=None):
        """Draws and continually updates the model obtained by calling `model_func` with `args` onto `canvas`."""
        self.canvas_map[canvas] = move
        self._animate_canvas(canvas, move)

    def _animate_canvas(self, canvas, move=None):
        model = self.model if move is None else self.model.get_next_state(move)
        self.draw_canvas(canvas, model)
        canvas.after(self.fps, self._animate_canvas, canvas, move)

    def draw_canvas(self, canvas: tk.Canvas, model: ViewModel):
        """Draws `model` onto `canvas`."""
        grid = model.get_grid()

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

        if model.get_game_over():
            title_font = (self.title_font[0], int(canvas_size/9*(self.title_font[1])), self.title_font[2])
            canvas.create_rectangle(0, 0, canvas_size, canvas_size, width=0, fill=GAME_OVER_STIPPLE, stipple='gray50')
            canvas.create_text(canvas_size/2, canvas_size/2, fill=TITLE, font=title_font, text='GAME OVER')

if __name__ == '__main__':
    root = tk.Tk()
    game = GameState()

    view = View(game, root)
    view.mainloop()