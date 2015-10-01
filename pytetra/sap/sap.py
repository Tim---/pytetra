
class Sap:
    def __init__(self):
        self.listeners = []

    def send(self, primitive):
        for l in self.listeners:
            l.recv(primitive)

    def register(self, listener):
        self.listeners.append(listener)
