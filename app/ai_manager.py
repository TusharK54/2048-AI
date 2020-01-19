
from queue import Queue
from ai.players import *

from messaging import QueueManager

class PlayerManager(QueueManager):
    def __init__(self, app_queue: Queue):
        self.app_queue = app_queue

        # Initialize internal AI

        QueueManager.__init__(self)
        self.launch_queue()

    def handle_event(self, event, data):
        if event == 'make move':
            pass
        elif event == 'select ai':
            pass

        else:
            raise Exception