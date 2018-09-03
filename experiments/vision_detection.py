# -*- encoding: UTF-8 -*-
#

from naoqi import ALProxy
import numpy as np
import cv2
import sys
import time


def get_img(robotIP, PORT):
    try:
        vision = ALProxy('RobocupVision', robotIP, PORT)
    except Exception, e:
        print "Could not create proxy to RobocupVision"
        print "Error was: ", e
        sys.exit(1)

    cameraId = 0

    data = vision.getBGR24Image(cameraId)
    image = np.frombuffer(data, dtype=np.uint8).reshape((480, 640, 3))

    cv2.imshow("Mask", image)
    cv2.waitKey(10000)
    cv2.imwrite('messigray.png', image)

    return image

def get_head_angles(robotIP, PORT):
    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)

    names         = "Head"
    useSensors  = True
    HeadAngles = motionProxy.getAngles(names, useSensors)

    return HeadAngles

def set_head_angles(robotIP, PORT, angles):
    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)

    motionProxy.setStiffnesses("Head", 1.0)
    # Example showing how to set angles, using a fraction of max speed
    names  = ["HeadYaw", "HeadPitch"]
    #angles  = [0.2, -0.2]
    fractionMaxSpeed  = 0.1
    motionProxy.setAngles(names, angles, fractionMaxSpeed)

    time.sleep(3.0)
    motionProxy.setStiffnesses("Head", 0.0)

def detect_red_blob(image):
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


if __name__ == "__main__":
    robotIP = "nao5.local"
    PORT = 9559
    camera_height = 523,23 #camera_height in mm


    image = get_img(robotIP, PORT)
    coordinates = detect_red_blob(image)
    angles = get_head_angles(robotIP, PORT) #+ 1.2 #the camera has an 1.2 degree angle to the head
    print(angles)
    #compute angle if point not in center of image (640 x 480)

    #distance = camera_height/ tan (90-head_angle)
    distance = camera_height/np.tan(90-angles) #TODO get tan correclty