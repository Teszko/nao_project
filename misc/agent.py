import time
import robot
import vision
# import gamepad
from commandqueue import CommandQueue
from speechqueue import SpeechQueue
import commands
import numpy as np
#import math
from recognizer import Recognizer
from threading import Thread

class Sense:
    def __init__(self, agent):
        self.posestate = "rest"  # "rest" or "ready"
        self.controlstate = "controlled"  # "controlled" or "indep"
        self.agent = agent
        self.target = None
        self.image = None
        self.__recognizer = Recognizer()
        self.__recognizer.on_keyword = self.on_keyword
        self.__thread = Thread(target = self.__recognizer.run)

        self.scan_state = 0

    def tick(self):
        # self.agent.pad.poll()

        if not self.__thread.isAlive() and self.agent.think.opmode in ['waiting']:
            self.__thread.start()

    def on_keyword(self, keyword):
        self.agent.speechQueue.reset()
        self.agent.speechQueue.add_element(keyword)


class Think:
    def __init__(self, agent):
        self.opmode = "waiting"  # "waiting" "searching" "moving" or "done"
        self.agent = agent
        self.head_yaw_step = 0.4
        self.camera = 0
        self.first_found = 0
        self.no_scan = 0
        self.scan_done = 0

    def reset_scan(self):
        self.first_found = 0
        self.agent.sense.scan_state = 0
        self.scan_done = 0
        print "queue add init_scan on reset"
        self.agent.commandQueue.add_element(commands.init_scan)

    def tick(self):
        if self.opmode == "waiting":
            speech = self.agent.speechQueue.pop_element()
            if speech:
                self.agent.sense.target = speech
                self.opmode = "searching"
                self.agent.robot.say("set opmode to searching")
        elif self.opmode == "searching":
            if self.agent.sense.posestate == "rest":
                print "queue add pose_ready"
                self.agent.commandQueue.add_element(commands.pose_ready)
                print "queue init_scan"
                self.agent.commandQueue.add_element(commands.init_scan)

            if (not self.first_found) and (not self.agent.sense.scan_state):
                self.agent.sense.scan_state = 1
                print "queue add scan view step 1"
                self.agent.commandQueue.add_element(commands.scan_view_step)

            img = self.agent.sense.image
            if img is not None:
                distance, angle = vision.detect_blob(self.agent, self.camera)
                print "distance, angle ", distance, " . ", angle
                if distance != -1:
                    self.agent.robot.say("distance " + str(np.around(distance, 1)))
                    self.no_scan = 1
                    print "queue add look straight 1"
                    self.agent.commandQueue.add_element(commands.look_straight)
                    self.first_found = 1
                    if distance <= 1.8 and self.camera == 0:
                        self.agent.robot.say("switching camera")
                        self.camera = 1
                    elif distance <= 0.6 and self.camera == 1:
                        print "queue add go to 1"
                        self.agent.commandQueue.add_element(commands.go_to(distance, angle))
                        self.opmode = "done"
                        return
                    self.opmode = "moving"
                    if self.camera == 0 and distance > 1:
                        distance = 1
                    if self.camera == 1 and distance > 0.5:
                        distance = 0.5

                    print "queue add go to 2"
                    self.agent.commandQueue.add_element(commands.go_to(distance, angle)) #angle = HeadYaw, distance in m
                    print "queue add scan front"
                    self.agent.commandQueue.add_element(commands.scan_front)
                else:
                    print "distance -1"
                    if self.scan_done == 1:
                        self.scan_done = 0
                        self.no_scan = 1
                        print "restart scan"
                        newcam = 1 - self.camera
                        self.agent.robot.say("nothing found switching to camera " + str(newcam))
                        #print "switching camera ", newcam
                        self.camera = newcam
                        self.reset_scan()

                self.agent.sense.image = None
                # handle image
                # if target found, set opmode to moving
        elif self.opmode == "moving":
            pass
            # handle moving
        elif self.opmode == "done":
            if not self.agent.sense.posestate == "rest":
                print "queue add pose rest"
                self.agent.sense.posestate = "rest"
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
        self.robot = robot.Robot(self)
        # self.pad = gamepad.Pad(self)
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
