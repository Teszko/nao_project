from __future__ import print_function
import motion
from naoqi import ALProxy
import sys
import cv2
import numpy as np


class Robot:
    """hardware abstraction."""
    def __init__(self):
        self.ip = "nao6.local"
        self.port = 9559
        self.initProxy()
        self.fractionMaxSpeed = 0.8
        self.motion = None
        self.vision = None
        self.tts = None

    def initProxy(self):
        try:
            self.motion = ALProxy("ALMotion", self.ip, self.port)
        except Exception, e:
            print("Could not create proxy to ALMotion")
            print("Error was: ", e)
            sys.exit(1)

        try:
            self.vision = ALProxy('RobocupVision', self.ip, self.port)
        except Exception, e:
            print("Could not create proxy to RobocupVision")
            print("Error was: ", e)
            sys.exit(1)

        try:
            self.tts = ALProxy("ALTextToSpeech", self.ip, self.port)
        except Exception, e:
            print("Could not create proxy to ALTextToSpeech")
            print("Error was: ", e)
            sys.exit(1)

    def get_img(self):
        cameraId = 0

        data = self.vision.getBGR24Image(cameraId)
        image = np.frombuffer(data, dtype=np.uint8).reshape((480, 640, 3))

        #cv2.imshow("Mask", image)
        #cv2.waitKey(10000)
        #cv2.imwrite('messigray.png', image)

        return image

    def wake(self):
        self.motion.wakeUp()

    def initPose(self):
        self.motion.moveInit()

    def say(self, s):
        print(">", s)
        self.tts.say(s)

    def rest(self):
        self.motion.rest()

    def move(self, x, y, theta):
        self.motion.move(x, y, theta)

    def go_to(self, distance, angle):
        self.motion.moveTo(distance, 0, angle)

    def set_head_angles(self, angles):
        names = ["HeadYaw", "HeadPitch"]
        # angles  = [0.2, -0.2]
        fractionMaxSpeed = 0.1
        self.motion.setAngles(names, angles, fractionMaxSpeed)

    def get_head_angle(self):
        names = "Head"
        HeadAngles = self.motion.getAngles(names, True)
        return HeadAngles

        # https://github.com/Teszko/programming-humanoid-robot-in-python/blob/master/nao_doc/motion.rst
        # getAngles(names, useSensors)
        # self.motion.getAngles

