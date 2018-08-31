from __future__ import print_function
import pygame

pygame.init()
pygame.joystick.init()


joystick_count = pygame.joystick.get_count()
joystick=None

print("Number of joysticks: {}".format(joystick_count))

for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

while True:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

        axes = joystick.get_numaxes()
        for i in range(axes):
            axis = joystick.get_axis(i)
            print("Axis {} value: {:>6.3f}".format(i, axis), end=" ")

        buttons = joystick.get_numbuttons()
        print("Number of buttons: {}".format(buttons) )

        for i in range( buttons ):
            button = joystick.get_button( i )
            #print("Button {:>2} value: {}".format(i, button))

        print("")