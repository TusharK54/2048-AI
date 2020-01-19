
import tkinter as tk
from threading import Thread
from queue import Queue
from math import log

from app.model import ViewModel
from app.messaging import QueueManager
from app.gui_colors import *

class View(QueueManager):

    def __init__(self, event_queue: Queue, master=None):
        # Should launch both other views

        QueueManager.__init__(self)
        self.launch_queue()


class GameView(tk.Frame, QueueManager):

    def __init__(self, model: ViewModel, event_queue: Queue=None, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky='nsew')

        self.state = model
        self.event_queue = event_queue

        control_panel = self.create_control_panel(150)
        canvas_panel = self.create_game_canvas(500)
        ai_panel = self.create_ai_panel(300)

        control_panel.grid(sticky='nsew', row=0, column=0)
        canvas_panel.grid(sticky='nsew', row=1, column=0)
        ai_panel.grid(sticky='nsew', row=0, column=1, rowspan=2)

        QueueManager.__init__(self)
        self.launch_queue()

    def new_handle_event(self, event, data):
        if event == 'activate ai button':
            pass
        elif event == 'deactivate ai button':
            pass
        elif event == 'lock ai button':
            pass
        elif event == 'unlock ai button':
            pass

        else:
            raise Exception

    def handle_event(self, event, data):
        if event == 'new game':
            self.ai_button.configure(state=tk.NORMAL)
        elif event == 'activate ai':
            self.ai_button.configure(text='Disable AI', bg=ENABLED_STANDARD_BUTTON)
        elif event == 'deactivate ai':
            self.ai_button.configure(text='Enable AI', bg=DEFAULT_STANDARD_BUTTON)
        elif event == 'game over':
            self.ai_button.configure(state=tk.DISABLED, text='Enable AI', bg=DEFAULT_STANDARD_BUTTON)
            
        else:
            raise Exception

    def create_control_panel(self, height: int):
        margin = 3
        panel = tk.Frame(self, height=height, bg=INFO_BACKGROUND, padx=margin, pady=margin)

        # 2048 title
        title = tk.Label(panel, text='2048', font=('Arial', 48, 'bold'), fg=TITLE, bg=INFO_BACKGROUND, padx=0, pady=0, bd=0)
        #title = tk.Canvas(panel, bg=INFO_BACKGROUND, bd=0)
        #text = title.create_text(15, -8, text='2048', fill=TITLE, font=('Arial', 50, 'bold'), anchor='nw')
        #bbox = title.bbox(text)  # get text bounding box
        #title.configure(width=bbox[2], height=bbox[3] - 30)

        # Score boxes
        score_box1 = tk.Frame(panel, bd=0, bg=SCORE_BOX)
        score_box2 = tk.Frame(panel, bd=0, bg=SCORE_BOX)

        score_label1 = tk.Label(score_box1, text='SCORE', width=7, bd=0, fg=SCORE_TITLE, bg=SCORE_BOX, font=('Arial', 12, 'bold'))
        score_label2 = tk.Label(score_box2, text='BEST', width=7, bd=0, fg=SCORE_TITLE, bg=SCORE_BOX, font=('Arial', 12, 'bold'))

        score_val1 = tk.Label(score_box1, textvariable=self.state.get_score_var(), bd=0, fg=BUTTON_LABELS, bg=SCORE_BOX, font=('Arial', 20, 'bold'))
        score_val2 = tk.Label(score_box2,  textvariable=self.state.get_best_var(), bd=0, fg=BUTTON_LABELS, bg=SCORE_BOX, font=('Arial', 20, 'bold'))

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
            size_button = tk.Radiobutton(size_buttons, variable=self.state.get_size_var(), value=i, text=i, command=lambda: self.event_queue.put('new game'), indicatoron=0, width=2, bg=DEFAULT_SIZE_BUTTON, fg=BUTTON_LABELS, activeforeground=BUTTON_LABELS, activebackground=ENABLED_SIZE_BUTTON, selectcolor=ENABLED_SIZE_BUTTON, font=('Arial', 10, 'bold'), bd=0, relief=tk.FLAT)
            size_button.grid(row=0, column=i, sticky='nsew')
            size_buttons.columnconfigure(i, weight=1)
        size_buttons.rowconfigure(0, weight=1)

        # Standard buttons
        button1 = tk.Button(panel, width=8, bd=0, font=('Arial', 10, 'bold'), relief=tk.FLAT, fg=BUTTON_LABELS, bg=DEFAULT_STANDARD_BUTTON, disabledforeground=BUTTON_LABELS, activeforeground=BUTTON_LABELS, activebackground=PRESSED_STANDARD_BUTTON, text='New Game', command=lambda: self.event_queue.put('new game', self.state.get_size_var().get()))
        button2 = tk.Button(panel, width=8, bd=0, font=('Arial', 10, 'bold'), relief=tk.FLAT, fg=BUTTON_LABELS, bg=DEFAULT_STANDARD_BUTTON, disabledforeground=BUTTON_LABELS, activeforeground=BUTTON_LABELS, activebackground=PRESSED_STANDARD_BUTTON, text='Enable AI', command=lambda: self.event_queue.put('toggle ai'))
        self.ai_button = button2

        # Position general widgets into place
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
        self.canvas = tk.Canvas(self, width=size, height=size, bg=TILE_GRID, bd=0, highlightthickness=0, cursor='crosshair')

        self.canvas_size = size
        self.update_canvas()

        return self.canvas

    def update_canvas(self):
        self.canvas.delete("all")

        grid = self.state.get_grid()
        grid_size = len(grid)

        margin = self.canvas_size/grid_size/10
        tile_size = (self.canvas_size - margin * (grid_size + 1)) / grid_size
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

                self.canvas.create_rectangle(x0, y0, x1, y1, width=0, fill=tile_color)
                self.canvas.create_text((x0+x1)/2, (y0+y1)/2, text=tile, fill=text_color, justify='center', font=('Helvetica Neue', int(text_size), 'bold'))

        if self.state.get_game_over():
            self.canvas.create_rectangle(0, 0, self.canvas_size, self.canvas_size, width=0, fill=GAME_OVER_STIPPLE, stipple='gray50')
            self.canvas.create_text(self.canvas_size/2, self.canvas_size/2-25, fill=TITLE, font=('Arial', 50, 'bold'), text='Game Over')
            self.canvas.create_text(self.canvas_size/2, self.canvas_size/2+25, fill=TITLE, font=('Arial', 15, 'bold'), text='Press [ENTER] to play again')

        fps = 15
        self.canvas.after(1000//fps, self.update_canvas)

    def create_ai_panel(self, width: int):
        panel = tk.Frame(self, width=width, bg='blue')
        panel.grid_propagate(0)
        
        return panel

class AiView(tk.Frame, QueueManager):

    def __init__(self, event_queue: Queue, master=None):
        tk.Frame.__init__(self, master)

        vis_panel = self.create_canvas()
        control_panel = self.create_control_panel()

    def handle_event(self, event, data):
        """Handles the following events: 
        `'update state'` `data` = new state
        """

    def create_control_panel(self) -> tk.Frame:
        pass

    def create_canvas(self) -> tk.Frame:
        pass

    def update_canvas(self, state) -> tk.Frame:
        pass

if __name__ == '__main__':
    root = tk.Tk()
    model = ViewModel()
    queue = Queue()

    view = View(model, queue, root)
    view.mainloop()