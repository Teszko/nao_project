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
        self.target = None
        self.image = None
        self.__scan_state = 0

    def tick(self):
        self.agent.pad.poll()
        # poll speech rec and add text to speechqueue if command given


class Think:
    def __init__(self, agent):
        self.opmode = "waiting"  # "waiting" "searching" "moving" or "done"
        self.agent = agent
        self.head_yaw_step = 0.2

    def tick(self):
        speech = self.agent.speechQueue.pop_element()
        if speech:
            pass
            # process text
        elif self.opmode == "waiting":
            speech = self.agent.speechQueue.pop_element()
            if speech:
                pass
                # handle command
        elif self.opmode == "searching":
            if self.agent.sense.posestate == "rest":
                self.agent.commandQueue.add_element(commands.pose_ready)

            if not self.agent.sense.__scan_state:
                self.agent.sense.__scan_state = 1
                self.agent.commandQueue.add_element(commands.scan_view_step)

            img = self.agent.sense.image
            if img:
                pass
                # handle image
                # if target found, set opmode to moving
        elif self.opmode == "moving":
            pass
            # handle moving
        elif self.opmode == "done":
            self.agent.commandQueue.add_element(commands.pose_rest)
            # handle done
            # pose rest


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