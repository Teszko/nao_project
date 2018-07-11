from __future__ import print_function
import pygame
from naoqi import ALProxy
import sys
import time

class Robot:
    def __init__(self):
        self.ip = "nao6.local"
        self.port = 9559
        self.initProxy()
        self.fractionMaxSpeed = 0.8

    def initProxy(self):
        try:
            self.motion = ALProxy("ALMotion", self.ip, self.port)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e
            sys.exit(1)

    def wake(self):
        self.motion.wakeUp()

    def initPose(self):
        self.motion.moveInit()

    def rest(self):
        self.motion.rest()

    def move(self, x, y, theta):
        self.motion.moveToward(x, y, theta, 0.6)


class Pad(object):
    def __init__(self, robot):
        pygame.init()
        pygame.joystick.init()

        self.robot = robot

        self.joystick_count = pygame.joystick.get_count()
        self.joystick = None

        self.stickL0 = 0
        self.stickL1 = 0
        self.stickR0 = 0
        self.stickR1 = 0

        self.toggleStart = 0

        self.init_joystick()

        print("Number of joysticks: {}".format(self.joystick_count))

    def start_pressed(self):
        print("start pressed")
        self.toggleStart = 1 - self.toggleStart

        if self.toggleStart:
            robot.wake()
            robot.initPose()
        else:
            robot.rest()


    def init_joystick(self):
        for i in range(self.joystick_count):
            self.joystick = pygame.joystick.Joystick(i)
            self.joystick.init()

    def getAxis(self, a):
        value = self.joystick.get_axis(a)
        if (value < 0.15) and (value > -0.15):
            value = 0
        return -1 * value

    def poll(self):
        '''
         for i in range( axes ):
            axis = joystick.get_axis( i )
            print("Axis {} value: {:>6.3f}".format(i, axis))
        '''
        for event in pygame.event.get():  # User did something
            if event.type == pygame.JOYBUTTONDOWN:
                if self.joystick.get_button(7):
                    self.start_pressed()

        self.stickL0 = self.getAxis(0)
        self.stickL1 = self.getAxis(1)
        self.stickR0 = self.getAxis(2)
        self.stickR1 = self.getAxis(3)

    def jprint(self):
        print("L0:", "{:>6.3f}".format(self.stickL0), " L1:", "{:>6.3f}".format(self.stickL1), "R0:", "{:>6.3f}".format(self.stickR0))

if __name__ == "__main__":
    robot = Robot()
    pad = Pad(robot)

    while True:
        pad.poll()
        pad.jprint()
        robot.move(pad.stickL1, pad.stickL0, pad.stickR0)
        time.sleep(0.1)
