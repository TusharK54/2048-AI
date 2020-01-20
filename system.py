
import tkinter as tk
from threading import Thread
from time import sleep # TODO: remove

from pub_sub import Publisher

from ai import BasePlayer, RandomPlayer
from game import Move, Game
from gui import View

class KeyboardManager(Publisher):

    def __init__(self, master):
        Publisher.__init__(self)
        master.bind('<Any-KeyPress>', self.keypress_handler)

    def handle_event(self, event, data):
        raise Exception

    def keypress_handler(self, key):
        symbol = key.keysym.lower()

        if symbol == 'return':
            self.publish_event('keypress enter')
        elif symbol == 'w' or symbol == 'up':
            self.publish_event('move', Move.UP)
        elif symbol == 's' or symbol == 'down':
            self.publish_event('move', Move.DOWN)
        elif symbol == 'a' or symbol == 'left':
            self.publish_event('move', Move.LEFT)
        elif symbol == 'd' or symbol == 'right':
            self.publish_event('move', Move.RIGHT)

class StateManager(Publisher):

    def __init__(self, state: Game=None):
        Publisher.__init__(self)
        self.model = state if state is not None else Game()

    def handle_event(self, event, data):
        if event == 'new game':
            self.model = Game(data)
            self.publish_event('update state', self.model)
        elif event == 'keyboard move':
            self.make_move(data)
        elif event == 'ai move':
            self.make_move(data)
        elif event == 'view enable ai':
            self.publish_event('enable ai', self.model)
        elif event == 'view disable ai':
            self.publish_event('disable ai')
        elif event == 'keypress enter':
            pass

        else:
            raise Exception

    def make_move(self, move: Move):
        if self.model.game_over():
            return

        self.model.make_move(move)
        if self.model.game_over():
            self.publish_event('disable ai')

class AIManager(Publisher):

    def __init__(self):
        Publisher.__init__(self)
        self.ai : BasePlayer = None

    def handle_event(self, event, data):
        if event == 'update state':
            pass
        elif event == 'enable ai':
            self.launch_ai(data)
        elif event == 'disable ai':
            self.kill_ai()
        elif event == 'select ai':
            pass

        else:
            raise Exception

    def launch_ai(self, state: Game):
        self.ai = RandomPlayer(state) #TODO: factory method

        worker = Thread(target=self.run_ai, daemon=True)
        worker.start()

    def run_ai(self):
        while self.ai is not None:
            if self.ai.get_game_state().game_over():
                self.publish_event('view disable ai')
                break

            move = self.ai.make_next_move()
            self.publish_event('ai move', move)
            self.publish_event('update ai', self.ai)

    def kill_ai(self):
        self.ai = None

class Application(object):

    def __init__(self):
        state = Game()

        # Initialize tkinter thread
        root = tk.Tk()

        # Initialize distributed components
        self.control = StateManager(state)
        self.keyboard = KeyboardManager(root)
        self.view = View(state, root)
        self.ai = AIManager()

        # Set up subscriptions
        connected = [self.control, self.view, self.ai]
        for i, component1 in enumerate(connected):
            for j, component2 in enumerate(connected):
                if i != j:
                    component1.subscribe(component2)

        self.control.subscribe(self.keyboard)

    def launch(self):
        self.control.launch_thread()
        self.ai.launch_thread()
        self.view.launch_thread() # NOTE: blocking thread

if __name__ == '__main__':
    app = Application()
    app.launch()