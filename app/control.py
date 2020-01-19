
from queue import Queue
from threading import Thread
import tkinter as tk
from ai.players import RandomPlayer
from game.game import Move

from .messaging import QueueManager
from .model import ControlModel
from .gui import View

class Application(QueueManager):

    def __init__(self):
        root = tk.Tk()
        self.model = ControlModel()

        QueueManager.__init__(self)
        view = View(self.model, self.queue(), root)
        self.view_queue = view.queue()
        
        #ai = RandomPlayer()
        #self.ai_queue = ai.queue()

        # Bind keyboard input to keypress handler in root window
        root.bind('<Any-KeyPress>', self.keypress_handler)

        self.launch_queue()
        view.mainloop()

    def new_handle_event(self, event, data):
        if event == 'keypress':
            pass
        elif event == 'ai move':
            pass
        elif event == 'new game':
            pass
        elif event == 'toggle ai':
            pass
        elif event == 'enable ai':
            pass
        elif event == 'disable ai':
            pass
        elif event == 'step ai':
            pass

        else:
            raise Exception

    def handle_event(self, event, data):
        if event == 'new game':
            self.model.new_game(data)
            self.view_queue.put('new game')

        elif event == 'toggle ai':
            self.model.set_ai(not self.model.get_ai())
            self.queue('trigger ai')
            if self.model.get_ai():
                self.view_queue.put('activate ai')
            else:
                self.view_queue.put('deactivate ai')

        elif event == 'move':
            if self.model.move_tiles(data):
                self.view_queue.put('update ui')
            if self.model.get_game_over():
                self.model.set_ai(False)
                self.view_queue.put('game over')

        elif event == 'trigger ai':
            if self.model.get_ai() and not self.model.get_game_over():
                state = self.model.get_board()
                self.ai_queue.put('make move', state)

        elif event == 'ai move':
            self.queue('move', data)
            self.queue('trigger ai')

        else:
            raise Exception

    def keypress_handler(self, key):
        symbol = key.keysym.lower()

        if symbol == 'return':
            if self.model.get_game_over():
                self.queue('new game')
            else:
                self.queue('toggle ai')

        if not (self.model.get_ai() or self.model.get_game_over()):
            if symbol == 'w' or symbol == 'up':
                self.queue('move', Move.UP)
            elif symbol == 's' or symbol == 'down':
                self.queue('move', Move.DOWN)
            elif symbol == 'a' or symbol == 'left':
                self.queue('move', Move.LEFT)
            elif symbol == 'd' or symbol == 'right':
                self.queue('move', Move.RIGHT)

if __name__ == '__main__':
    app = Application()