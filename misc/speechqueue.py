
class SpeechQueue:
    def __init__(self):
        self.reset()

    def add_element(self, str):
        self.queue.append(str)

    def pop_element(self):
        if len(self.queue):
            return self.queue.pop(0)
        else:
            return None

    def reset(self):
        self.queue = ["blue"]
