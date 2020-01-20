"""
This module contains all the components required to implement a single message queue for a distributed system.

Any class that needs to implement a message queue should inherit the `QueueManager` class and define the `handle_event()` method. To launch the message queue handler, the class should call the `launch_queue()` method. This will immediately launch a worker thread to start handling events in the message queue. Since event handling might need to reference properties of the class, it is recommended to call `launch_queue()` as the last step of the subclass initialization, after all the other properties have been initialized.
"""

import json
from abc import ABC, abstractmethod
from queue import Queue
from threading import Thread

class MessageQueue(Queue):

    def __init__(self):
        Queue.__init__(self)

    def put(self, event, data=None):
        """Add an event, optionally with some associated data, to the end of the queue."""
        super().put((event, data))

class QueueManager(ABC):

    def __init__(self):
        self.message_queue = MessageQueue()

    def queue(self, event=None, data=None):
        """Return this object's message queue and optionally add an event to the queue."""
        if event is not None:
            self.message_queue.put(event, data)
        return self.message_queue

    def launch_thread(self):
        """Launch a worker thread to handle events in the message queue."""
        worker = Thread(target=self._queue_handler, daemon=True)
        worker.start()

    def kill_thread(self):
        """Add an event to the message queue that will kill the worker thread once it is handled.""" 
        self.message_queue.put(None)

    def get_id(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def handle_event(self, event, data):
        """Handle the given event with the provided data. Raise an exception if an unknown event is encountered."""
        pass

    def _queue_handler(self):
        """Continually handle events from the message queue until `None` is encountered."""
        while True:
            try:
                item = self.message_queue.get()
                if item is None:
                    print(self.get_id(), 'is shutting down')
                    break
                
                event, data = item
            except Exception:
                print('--ERROR--', self.get_id(), 'skipping invalid item:', item)
            else:
                try:
                    self.handle_event(event, data)
                except Exception:
                    print('--ERROR--', self.get_id(), 'skipping unrecognized event:', item)
                else:
                    print(self.get_id(), 'handled event:', item)