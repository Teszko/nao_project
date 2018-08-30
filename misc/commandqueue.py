import command
import threading


class CommandQueue:
    def __init__(self, agent):
        self.current = None
        self.agent = agent
        self.queue = []

    def tick(self):
        if self.current:
            if self.current.isAlive():
                return

        if len(self.queue):
            elem = self.queue.pop(0)
            self.current = threading.Thread(target=elem.run, args=(self.agent,))

    def add_element(self, func):
        el = command.Command(self.agent)
        el.run = func
        self.queue.append(el)
