import time
import robot
import gamepad
from commandqueue import CommandQueue


class Sense:
    def __init__(self, agent):
        self.posestate = "rest"  # "rest" or "ready"
        self.controlstate = "controlled"  # "controlled" or "indep"
        self.agent = agent

    def tick(self):
        self.agent.pad.poll()


class Think:
    def __init__(self, agent):
        self.agent = agent

    def tick(self):
        pass


class Act:
    def __init__(self, agent):
        self.agent = agent

    def tick(self):
        self.agent.queue.tick()
        time.sleep(0.1)


class Agent:
    def __init__(self):
        self.sense = Sense(self)
        self.think = Think(self)
        self.act = Act(self)
        self.robot = robot.Robot()
        self.pad = gamepad.Pad(self)
        self.queue = CommandQueue(self)

    def sense_think_act(self):
        self.sense.tick()
        self.think.tick()
        self.act.tick()

    def run(self):
        while True:
            self.sense_think_act()