
import tkinter as tk
from threading import Thread
from time import sleep # TODO: remove

from messaging import PubSub

from ai import BaseAI, DummyAI
from game import Move, GameState
from gui import View

class KeyboardManager(PubSub):
    """Captures keyboard presses and publishes them as events."""

    def __init__(self, master):
        PubSub.__init__(self)
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

class GameManager(PubSub):
    """Contains and manages game state."""

    def __init__(self, game: GameState):
        PubSub.__init__(self)
        self.game_state = game

    def handle_event(self, event, data):
        if event == 'restart':              # data contains size
            self.game_state = GameState(data)
            self.publish_event('new game', self.game_state)
        elif event == 'keyboard move':      # data contains move
            if not self.game_state.game_over():
                self.game_state.update_state(data)
        else:
            raise Exception

class AIManager(PubSub):
    """Contains and manages AI state."""

    def __init__(self, ai: BaseAI):
        PubSub.__init__(self)
        self.ai_state = ai
        self.running = False

    def handle_event(self, event, data):
        if event == 'new game':             # data contains new game state
            self.new_game(data)
        elif event == 'start ai':
            self.start()
        elif event == 'stop ai':
            self.stop()
        elif event == 'step ai':
            self.step()
        elif event == 'run':
            self.run()
        else:
            raise Exception

    def new_game(self, game: GameState):
        self.stop()
        self.ai_state = DummyAI(game) # TODO: factory method
        self.publish_event('ai new', self.ai_state)
        self.publish_event('toggle ai', False)

    def start(self):
        if not self.ai_state.game_state.game_over():
            self.running = True
            self.publish_event('toggle ai', True)
            self.queue('run')

    def stop(self):
        self.running = False
        self.publish_event('toggle ai', False)

    def step(self):
        if not self.ai_state.game_state.game_over():
            self.ai_state.make_move()

    def run(self):
       # sleep(100/1000)
        self.step()
        if self.ai_state.game_state.game_over():
            self.stop()
        elif self.running:
            self.queue('run')

class Application(object):

    def __init__(self):
        game = GameState()
        ai = DummyAI(game) # TODO: factory method

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
        self.ai_control.subscribe(self.view)
        self.view.subscribe(self.game_control)
        self.view.subscribe(self.ai_control)

    def launch(self):
        self.game_control.launch_thread()
        self.ai_control.launch_thread()
        self.view.launch_thread() # NOTE: blocking thread

if __name__ == '__main__':
    app = Application()
    app.launch()