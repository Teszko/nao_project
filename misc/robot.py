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

    def get_img(self):
        cameraId = 0

        data = self.vision.getBGR24Image(cameraId)
        image = np.frombuffer(data, dtype=np.uint8).reshape((480, 640, 3))

        cv2.imshow("Mask", image)
        cv2.waitKey(10000)
        cv2.imwrite('messigray.png', image)

        return image

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

    def detect_red_blob(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_red = np.array([5, 50, 50])
        upper_red = np.array([15, 255, 255])
        mask0 = cv2.inRange(img, lower_red, upper_red)
        cv2.imshow("Mask0", mask0)

        lower_red = np.array([170, 50, 50])
        upper_red = np.array([180, 255, 255])
        mask1 = cv2.inRange(img, lower_red, upper_red)
        cv2.imshow("Mask1", mask1)

        mask = mask0 + mask1
        cv2.imshow("Mask1", mask1)

        _, cnts, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # area1 and area2 are the range of contour area, change accordingly
        area1 = 100
        area2 = 2000000
        totalDots = []
        max_area = -100
        cnt_max = 0

        # Count the total number of contours
        for cnt in cnts:
            if area1 < cv2.contourArea(cnt) < area2:
                print(cv2.contourArea(cnt))
                if cv2.contourArea(cnt) > max_area:
                    max_area = cv2.contourArea(cnt)
                    cnt_max = cnt
                totalDots.append(cnt)

        # getting position of biggest blob
        if len(totalDots) > 0:
            (x, y), radius = cv2.minEnclosingCircle(cnt_max)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(img, center, radius, (0, 255, 0), 2)
            print("center:")
            print(center)
        else:
            print("no dots found!")
            return -1

        text = "Total number of dots are: {}".format(len(totalDots))
        cv2.putText(mask, text, (50, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 255, 255), 2)
        cv2.imshow("Mask", mask)
        cv2.waitKey(10000)
        cv2.destroyAllWindows()
        print("Total number of dots are:{}".format(len(totalDots)))

        return center