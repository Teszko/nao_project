from __future__ import print_function
import pygame


class Pad(object):
    """initializing and handling controller inputs."""
    def __init__(self, agent):
        pygame.init()
        pygame.joystick.init()

        self.agent = agent

        self.joystick_count = pygame.joystick.get_count()
        print(self.joystick_count)

        self.stickL0 = 0
        self.stickL1 = 0
        self.stickR0 = 0
        self.stickR1 = 0

        self.toggleStart = 0

        for i in range(self.joystick_count):
            self.joystick = pygame.joystick.Joystick(i)
            self.joystick.init()

        print("Number of joysticks: {}".format(self.joystick_count))

    def start_pressed(self):
        print("start pressed")
        self.toggleStart = 1 - self.toggleStart

        if self.toggleStart:
            self.agent.robot.wake()
            self.agent.robot.initPose()
        else:
            self.agent.robot.rest()

    def get_axis(self, a):
        value = self.joystick.get_axis(a)
        if (value < 0.15) and (value > -0.15):
            value = 0
        return -1 * value

    def poll(self):
        for event in pygame.event.get():  # User did something
            if event.type == pygame.JOYBUTTONDOWN:
                if self.joystick.get_button(7):
                    self.start_pressed()

        self.stickL0 = self.get_axis(0)
        self.stickL1 = self.get_axis(1)
        self.stickR0 = self.get_axis(2)
        self.stickR1 = self.get_axis(3)

    def jprint(self):
        print("L0:", "{:>6.3f}".format(self.stickL0), " L1:", "{:>6.3f}".format(self.stickL1), "R0:", "{:>6.3f}".format(self.stickR0))
