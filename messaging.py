"""
This module contains all the components required implement a distributed system using a publisher/subscriber protocol or a simple message queue protocol.

Any class that needs to implement a message queue should inherit the `QueueHandler` class and implement the `handle_event()` method as defined by its specification. To launch the message queue handler, the class should call the `launch_queue()` method. This will immediately launch a worker thread to start handling events in the message queue. Since event handling might need to reference properties of the class, it is recommended to call `launch_queue()` as the last step of the subclass initialization, after all the other properties have been initialized.

Any class that needs to send and recieve events selectively should inherit the `PubSub` class. This allows the class to selectively subscribe to other `PubSub` objects using the `subscribe()` method, and publish events to their own subscribers using the `publush_event()` method. 
"""

import json
from abc import ABC, abstractmethod
from queue import Queue
from threading import Thread

class Message(object):

    def __init__(self, event, data):
        self.event = event
        self.data = data

    def __repr__(self):
        s = repr(self.event)
        if self.data is not None:
            s += ', ' + repr(self.data)
        return s

class MessageQueue(Queue):

    def __init__(self):
        Queue.__init__(self)

    def put(self, event, data=None):
        """Add an event with some associated data to the end of the queue."""
        super().put(Message(event, data))

class QueueHandler(ABC):

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
                msg = self.message_queue.get()
                if msg is None:
                    print(self.get_id(), 'is shutting down')
                    break
                else:
                    event, data = msg.event, msg.data
            except Exception:
                print('--ERROR--', self.get_id(), 'skipping invalid item:', msg)
            else:
                try:
                    self.handle_event(event, data)
                except Exception:
                    print(self.get_id(), 'skipped event:', msg)
                else:
                    print(self.get_id(), 'handled event:', msg)
                    # TODO use logs instead of printing

class PubSub(QueueHandler):


    def __init__(self):
        QueueHandler.__init__(self)
        self.subscribers = []

    def subscribe(self, publisher):
        """Subscribe to another `PubSub` object."""
        publisher.add_subscriber(self)

    def publish_event(self, event, data=None):
        """Send `event` and `data` to all subscribers."""
        for subscriber in self.subscribers:
            subscriber.queue(event, data)

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)