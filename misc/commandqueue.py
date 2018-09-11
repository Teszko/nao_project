from __future__ import print_function
import threading


class QueueElement:
    """ wrapper to put a function plus optional comment in Queue
    """
    def __init__(self, fn, comment=""):
        self.fn = fn
        self.comment = comment


class CommandQueue:
    """ Command queue. saves a list of QueueElement and executes the first function
        in the Queue (fifo) in a thread. Only one can run at a time. Once it's finished,
        the next one starts running.
    """
    def __init__(self, agent):
        self.current = None
        self.current_comment = ""
        self.agent = agent
        self.queue = []
        self.lock = 0

    def tick(self):
        """ Checks if next element in queue needs to run.
        """
        # print("Q ", self.print_queue(10))
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
        """ Add a function to end of Queue

        Args:
            func: a function that only takes agent as an argument
            comment (optional): comment that describes what this element does. Helps understanding what is happening if you print the queue.
        """
        if not self.lock:
            qel = QueueElement(func, comment)
            self.queue.append(qel)

    def set_lock(self):
        """ Prevent elements from being added to queue.
        """
        self.lock = 1

    def unset_lock(self):
        """ Allows elements to be added to queue.
        """
        self.lock = 0

    def clear_queue(self):
        """ Empties the Queue. Currently running elements keep running.
        """
        self.queue = []

    def print_queue(self, max_q=100):
        """ Prints the Queue in a human readable fashion.

        Args:
            max_q (int, optional): maximum number of elements to print. cut off if more.
        """
        print("Q ("+str(len(self.queue))+": ", end="")
        if self.current is not None:
            print("| running <" + self.current_comment + "> | --- ", end="")
        else:
            print("|  | --- ", end="")

        for i in range(min(len(self.queue), max_q)):
            print(" | id " + str(i) + "<" + self.queue[i].comment + "> | ")

        print(" --- end\n\n")
