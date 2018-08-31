import time
import robot
import gamepad
from commandqueue import CommandQueue
from speechqueue import SpeechQueue
import commands


class Sense:
    def __init__(self, agent):
        self.posestate = "rest"  # "rest" or "ready"
        self.controlstate = "controlled"  # "controlled" or "indep"
        self.agent = agent
        self.image = None

    def tick(self):
        self.agent.pad.poll()
        # poll speech rec and add text to speechqueue if command given


class Think:
    def __init__(self, agent):
        self.opmode = "searching"  # "searching" or "moving"
        self.scan_state = "done" # "done" or "progress"
        self.agent = agent
        self.head_yaw_step = 0.4

    def tick(self):
        speech = self.agent.speechQueue.pop_element()
        if speech:
            pass
            # process text

        if self.opmode == "searching" and self.op_state == "done":
            self.agent.commandQueue.add_element(commands.scan_view_step)
            # add commend to queue to move head and get new image

        # analyze image here if sense.image not None
        # set sense.image = None if you are done.



class Act:
    def __init__(self, agent):
        self.agent = agent

    def tick(self):
        self.agent.commandQueue.tick()
        time.sleep(0.1)


class Agent:
    def __init__(self):
        self.sense = Sense(self)
        self.think = Think(self)
        self.act = Act(self)
        self.robot = robot.Robot()
        self.pad = gamepad.Pad(self)
        self.commandQueue = CommandQueue(self)
        self.speechQueue = SpeechQueue()

    def sense_think_act(self):
        self.sense.tick()
        self.think.tick()
        self.act.tick()

    def run(self):
        while True:
            self.sense_think_act()