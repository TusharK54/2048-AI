
import tkinter as tk
from threading import Thread
from time import sleep # TODO: remove

from pub_sub import Publisher

from ai import BasePlayer, RandomPlayer
from game import Move, GameState
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
            self.publish_event('keyboard move', Move.UP)
        elif symbol == 's' or symbol == 'down':
            self.publish_event('keyboard move', Move.DOWN)
        elif symbol == 'a' or symbol == 'left':
            self.publish_event('keyboard move', Move.LEFT)
        elif symbol == 'd' or symbol == 'right':
            self.publish_event('keyboard move', Move.RIGHT)

class GameManager(Publisher):

    def __init__(self, game: GameState=None):
        Publisher.__init__(self)
        self.game_state = game if game is not None else GameState()

    def handle_event(self, event, data):
        if event == 'restart':              # data contains size
            self.game_state = GameState(data)
            self.publish_event('new game', self.game_state)
        elif event == 'keyboard move':      # data contains move
            self.make_move(data)
            
        else:
            raise Exception

    def make_move(self, move: Move):
        if self.game_state.game_over():
            return

        self.game_state.update_state(move)
        
        if self.game_state.game_over():
            pass

class AIManager(Publisher):

    def __init__(self):
        Publisher.__init__(self)
        self.ai : BasePlayer = None

    def handle_event(self, event, data):
        if event == 'update game':
            pass
        elif event == 'enable ai':
            self.launch_ai(data)
        elif event == 'disable ai':
            self.kill_ai()
        elif event == 'select ai':
            pass

        else:
            raise Exception

    def launch_ai(self, game: GameState):
        self.ai = RandomPlayer(game) #TODO: factory method

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
        game = GameState()

        # Initialize tkinter thread
        root = tk.Tk()

        # Initialize distributed components
        self.control = GameManager(game)
        self.keyboard = KeyboardManager(root)
        self.view = View(game, root)

        # Set up subscriptions
        self.control.subscribe(self.keyboard)
        self.control.subscribe(self.view)
        self.view.subscribe(self.control)

    def launch(self):
        self.control.launch_thread()
        self.view.launch_thread() # NOTE: blocking thread

if __name__ == '__main__':
    app = Application()
    app.launch()
