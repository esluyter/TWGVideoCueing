"""
Publisher class

This is a superclass that implements the Observer pattern

Author: Eric Sluyter
Last edited: July 2018
"""

class Publisher:
    def __init__(self):
        self.subscribers = set()
    def register(self, who):
        self.subscribers.add(who)
    def unregister(self, who):
        self.subscribers.discard(who)
    def changed(self, what, etc=None):
        if self.role == 'model':
            for subscriber in self.subscribers:
                subscriber.model_update(what, etc)
        if self.role == 'view':
            for subscriber in self.subscribers:
                subscriber.view_update(what, etc)
