from __future__ import print_function
import threading


class QueueElement:
    def __init__(self, fn, comment=""):
        self.fn = fn
        self.comment = comment


class CommandQueue:
    def __init__(self, agent):
        self.current = None
        self.current_comment = ""
        self.agent = agent
        self.queue = []
        self.lock = 0

    def tick(self):
        print("Q ", self.print_queue(10))
        if self.current:
            if self.current.is_alive():
                return
            else:
                self.current = None

        if len(self.queue):
            qel = self.queue.pop(0)
            self.current = threading.Thread(target=qel.fn, args=(self.agent,))
            self.current_comment = qel.comment
            self.current.start()

    def add_element(self, func, comment=""):
        if not self.lock:
            qel = QueueElement(func, comment)
            self.queue.append(qel)

    def set_lock(self):
        self.lock = 1

    def unset_lock(self):
        self.lock = 0

    def clear_queue(self):
        self.queue = []

    def print_queue(self, max_q=100):
        print("Q ("+str(len(self.queue))+": ", end="")
        if self.current is not None:
            print("| running <" + self.current_comment + "> | --- ", end="")
        else:
            print("|  | --- ", end="")

        for i in range(min(len(self.queue), max_q)):
            print(" | id " + str(i) + "<" + self.queue[i].comment + "> | ")

        print(" --- end\n\n")