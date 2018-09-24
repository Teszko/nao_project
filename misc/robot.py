from __future__ import print_function
import motion
from naoqi import ALProxy
import sys
import cv2
import time
import numpy as np


class Robot:
    """hardware abstraction."""
    def __init__(self, agent):
        self.ip = "nao5.local"
        self.port = 9559
        self.fractionMaxSpeed = 0.8
        self.motion = None
        self.vision = None
        self.tts = None
        self.initProxy()
        self.agent = agent

    def initProxy(self):
        """ handles connection to Nao AL proxies.
        """

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
        """ takes an image with camera id in agent.think.camera

        Returns:
             image: image data (numpy matrix)
        """
        data = self.vision.getBGR24Image(self.agent.think.camera)
        image = np.frombuffer(data, dtype=np.uint8).reshape((480, 640, 3))

        #cv2.imshow("Mask", image)
        #cv2.waitKey(10000)
        #cv2.imwrite('messigray.png', image)

        return image

    def wake(self):
        """ sets actuator stiffness.
        """
        self.motion.wakeUp()

    def initPose(self):
        """ puts Nao into a pose where he's able to walk.
        """
        self.motion.moveInit()

    def say(self, s):
        """ say phrase

        Args:
            s (string): thing to say.
        """
        print(">", s)
        self.tts.say(s)

    def rest(self):
        """ puts Nao into resting position.
        """
        self.motion.rest()

    def move(self, x, y, theta):
        """ makes nao walk and turn with set speed. currently not used.
        """
        self.motion.move(x, y, theta)

    def go_to(self, distance, angle):
        """ first makes Nao turn in specific direction, then waits to stabilize and walks set distance forward."""
        self.motion.moveTo(0, 0, angle)
        time.sleep(2)
        self.motion.moveTo(distance, 0, 0)

    def set_head_angles(self, angles):
        """ moves head in specific direction.
        """
        names = ["HeadYaw", "HeadPitch"]
        # angles  = [0.2, -0.2]
        fractionMaxSpeed = 0.2
        self.motion.setAngles(names, angles, fractionMaxSpeed)

    def get_head_angle(self):
        """ returns current head orientation.
        """
        names = "HeadYaw"
        HeadAngles = self.motion.getAngles(names, True)
        return HeadAngles[0]

        # https://github.com/Teszko/programming-humanoid-robot-in-python/blob/master/nao_doc/motion.rst
        # getAngles(names, useSensors)
        # self.motion.getAngles

