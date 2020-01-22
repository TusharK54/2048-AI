"""
This module contains all the components required implement a distributed system using a publisher/subscriber protocol or a simple message queue protocol.

Any class that needs to implement a message queue should inherit the `QueueManager` class and define the `handle_event()` method. To launch the message queue handler, the class should call the `launch_queue()` method. This will immediately launch a worker thread to start handling events in the message queue. Since event handling might need to reference properties of the class, it is recommended to call `launch_queue()` as the last step of the subclass initialization, after all the other properties have been initialized.
"""

import json
from abc import ABC, abstractmethod
from queue import Queue
from threading import Thread

class Message(object):

    def __init__(self, event, data):
        self.event = event
        self.data = data

    def get(self):
        return self.event, self.data

    def __repr__(self):
        return repr(self.event) + ', ' + repr(self.data)

class MessageQueue(Queue):

    def __init__(self):
        Queue.__init__(self)

    def put(self, event, data):
        """Add an event, optionally with some associated data, to the end of the queue."""
        super().put(Message(event, data))

class QueueManager(ABC):

    def __init__(self):
        self.message_queue = MessageQueue()

    def queue(self, event, data=None):
        """Return this object's message queue and optionally add a message to the queue."""
        if event is not None:
            self.message_queue.put(event, data)
        return self.message_queue

    def launch_thread(self):
        """Launch a worker thread to handle events in the message queue."""
        worker = Thread(target=self._queue_handler, daemon=True)
        worker.start()

    def kill_thread(self):
        """Add a message to the message queue that will kill the worker thread once it is handled.""" 
        self.queue(None)

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
                
                event, data = item.get()
            except Exception:
                print('--ERROR--', self.get_id(), 'skipping invalid item:', item)
            else:
                try:
                    self.handle_event(event, data)
                except Exception as e:
                    print(self.get_id(), 'skipped event:', item)
                    raise e
                else:
                    print(self.get_id(), 'handled event:', item)

class Publisher(QueueManager): # TODO: change name

    def __init__(self):
        QueueManager.__init__(self)
        self.subscribers = []

    def publish_event(self, event, data=None):
        for subscriber in self.subscribers:
            subscriber.queue(event, data)

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)

    def subscribe(self, publisher):
        publisher.add_subscriber(self)