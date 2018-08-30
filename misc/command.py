class Command:
    def __init__(self, agent, func):
        # func is a function that gets passed agent as an argument
        self.agent = None
        self.run = func