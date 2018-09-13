import time
import robot
import vision
# import gamepad
from commandqueue import CommandQueue
from speechqueue import SpeechQueue
from states import StateMachine
import commands
import numpy as np
#import math
from recognizer import Recognizer
from threading import Thread


class Sense:
    """ Sense part of sense - think - act loop. Provides an interface to sensors.
    """
    def __init__(self, agent):
        self.posestate = "rest"  # "rest" or "ready"
        self.controlstate = "controlled"  # "controlled" or "indep"
        self.agent = agent
        self.target = None
        self.image = None
        self.__recognizer = Recognizer()
        self.__recognizer.on_keyword = self.on_keyword
        self.__thread = Thread(target=self.__recognizer.run)
        self.__ran = 0

    def tick(self):
        # self.agent.pad.poll()

        if (not self.__thread.is_alive()) and (self.agent.think.opmode in ['waiting']) and self.__ran == 0:
            self.__ran = 1
            self.__thread.start()

    def on_keyword(self, keyword):
        self.agent.speechQueue.reset()
        self.agent.speechQueue.add_element(keyword)


class Think:
    """ Think part of sense - think - act loop. Computes sensor output,
        controls robot behaviour. Adds actions to command queue.
    """
    def __init__(self, agent):
        self.opmode = "waiting"  # "waiting" "searching" "moving" or "done"
        self.agent = agent
        self.max_dist = 1.0
        self.head_yaw_step = 0.4
        self.camera = 0
        self.num_full_scans = 0
        self.finished_scan = 0
        self.scanning = 0
        self.walking = 0
        self.scan_type = 0  # 0 for wide scan, 1 for scan front
        self.found = 0

    def switch_camera(self):
        self.camera = 1 - self.camera
        self.agent.robot.say("switch camera to " + str(self.camera))

    def init_scan(self):
        self.scanning = 1
        self.found = 0
        self.finished_scan = 0
        self.scan_type = 0
        self.agent.commandQueue.add_element(commands.init_scan, "init scan a")
        self.agent.commandQueue.add_element(commands.scan_view_step, "scan view a")

    def done_scan(self):
        self.scanning = 0
        self.found = 1

    def walk_to_target(self, distance, angle):
        self.walking = 1
        self.agent.commandQueue.add_element(commands.look_straight, "look straight a")
        self.agent.commandQueue.add_element(commands.go_to(distance, angle), "go to dist " + str(np.around(distance, 1)) + ", angle " + str(np.around(angle, 1)))

    def tick(self):
        self.agent.stateMachine.tick()


class Act:
    """ Act part of sense - think - act loop. Runs elements in command queue.
    """
    def __init__(self, agent):
        self.agent = agent

    def tick(self):
        self.agent.commandQueue.tick()
        time.sleep(0.1)


class Agent:
    """ Agent, call sense - think - act loop.
    """
    def __init__(self):
        self.sense = Sense(self)
        self.think = Think(self)
        self.act = Act(self)
        self.robot = robot.Robot(self)
        # self.pad = gamepad.Pad(self)
        self.stateMachine = StateMachine(self)
        self.commandQueue = CommandQueue(self)
        self.speechQueue = SpeechQueue()

    def __enter__(self):
        self.run()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self.sense, '__thread'):
            self.sense.__thread.terminate()

    def sense_think_act(self):
        self.sense.tick()
        self.think.tick()
        self.act.tick()

    def run(self):
        while True:
            self.sense_think_act()
