
class SpeechQueue:
    def __init__(self):
        self.queue = ["red"]

    def add_element(self, str):
        self.queue.append(str)

    def pop_element(self):
        if len(self.queue):
            return self.queue.pop(0)
        else:
            return None
