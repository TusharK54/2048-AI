
import tkinter as tk
from threading import Thread
from time import sleep # TODO: remove

from pub_sub import Publisher

from ai import Base, Dummy, Dummy2
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

    def __init__(self, game: GameState):
        Publisher.__init__(self)
        self.game_state = game

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

    def __init__(self, ai: Base):
        Publisher.__init__(self)
        self.ai_state = ai

    def handle_event(self, event, data):
        if event == 'new game':             # data contains new game state
            self.ai_state = Dummy2(data) # TODO: factory method
            self.publish_event('new ai', self.ai_state)
        
        else:
            raise Exception

class Application(object):

    def __init__(self):
        game = GameState()
        ai = Dummy(game) # TODO: factory method

        # Initialize tkinter thread
        root = tk.Tk()

        # Initialize distributed components
        self.keyboard = KeyboardManager(root)
        self.game_control = GameManager(game)
        self.ai_control = AIManager(ai)
        self.view = View(game, ai, root)

        # Set up subscriptions
        self.game_control.subscribe(self.keyboard)
        self.game_control.subscribe(self.view)
        self.ai_control.subscribe(self.game_control)
        self.view.subscribe(self.game_control)
        self.view.subscribe(self.ai_control)

    def launch(self):
        self.game_control.launch_thread()
        self.ai_control.launch_thread()
        self.view.launch_thread() # NOTE: blocking thread

if __name__ == '__main__':
    app = Application()
    app.launch()
