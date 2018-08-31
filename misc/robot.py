from __future__ import print_function
import motion
from naoqi import ALProxy
import sys


class Robot:
    """hardware abstraction."""
    def __init__(self):
        self.ip = "nao6.local"
        self.port = 9559
        self.initProxy()
        self.fractionMaxSpeed = 0.8

    def initProxy(self):
        try:
            self.motion = ALProxy("ALMotion", self.ip, self.port)
        except Exception, e:
            print("Could not create proxy to ALMotion")
            print("Error was: ", e)
            sys.exit(1)

    def wake(self):
        self.motion.wakeUp()

    def initPose(self):
        self.motion.moveInit()

    def say(self):
        pass

    def rest(self):
        self.motion.rest()

    def move(self, x, y, theta):
        self.motion.move(x, y, theta)

    def get_head_angle(self):
        pass
        # https://github.com/Teszko/programming-humanoid-robot-in-python/blob/master/nao_doc/motion.rst
        # getAngles(names, useSensors)
        # self.motion.getAngles