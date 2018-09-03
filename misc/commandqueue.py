import threading


class CommandQueue:
    def __init__(self, agent):
        self.current = None
        self.agent = agent
        self.queue = []

    def tick(self):
        print "self.queue ", len(self.queue)
        if self.current:
            if self.current.is_alive():
                return

        if len(self.queue):
            func = self.queue.pop(0)
            self.current = threading.Thread(target=func, args=(self.agent,))
            self.current.start()

    def add_element(self, func):
        self.queue.append(func)
