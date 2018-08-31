from __future__ import print_function
import pygame
import time

class Pad(object):
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        self.joystick_count = pygame.joystick.get_count()
        self.joystick = None

        self.stickL0 = 0
        self.stickL1 = 0
        self.stickR0 = 0
        self.stickR1 = 0

        self.init_joystick()

        print("Number of joysticks: {}".format(self.joystick_count))

    def start_pressed(self):
        print("start pressed")

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

pad = Pad()

while True:
    pad.poll()
    pad.jprint()
    time.sleep(0.1)
