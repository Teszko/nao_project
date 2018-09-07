import cv2
import numpy as np
import random

def detect_blob(agent, camera):
    center = -1
    image = agent.sense.image
    color = agent.sense.target
    red = ([5, 50, 50], [15, 255, 255])
    blue = ([100,150,0], [140,255,255])


    if color == "red":
        center = get_blob_center(image, red)
    elif color == "blue":
        center = get_blob_center(image, blue)

    if center != -1:
        return get_distance(center, agent, camera)
    else:
        return -1, None


def get_blob_center(image, color):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_boundary = np.array(color[0])
    upper_boundary = np.array(color[1])
    mask = cv2.inRange(img, lower_boundary, upper_boundary)

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
    print("Total number of dots are:{}".format(len(totalDots)))

    cv2.imwrite("pic"+str(random.randint(0,1000))+".png", image)
    return center

def detect_blue_blob(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_boundary = np.array([100,150,0])
    upper_boundary = np.array([140,255,255])
    mask = cv2.inRange(img, lower_boundary, upper_boundary)
    #cv2.imshow("Mask0", mask0)


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
    #cv2.imshow("Mask", mask)
    #cv2.waitKey(10000)
    #cv2.destroyAllWindows()
    print("Total number of dots are:{}".format(len(totalDots)))

    return center


def get_distance(center, agent, camera):
    print "get distance"
    print center
    print "camera ", camera
    # get head_angles values
    anglesYaw = agent.robot.get_head_angle()
    # get y and y coordinates
    y_coordinate = center[1]

    # compute angle for points not in center of image (imagesize: 640 x 480)
    y_offset = 240 - y_coordinate


    anglesYaw = anglesYaw + ((y_offset * (60.97/ 480)) / 360 * 2 * 3.1415)  # 47.64 degrees in x direction

    if camera == 0:
        distance = float(480 - y_coordinate) * 2.5 / 240 + 0.85
    elif camera == 1:
        distance = 2 * float(480 - y_coordinate) * 0.46 / 240 + 0.22
    else:
        distance = -1

    return distance, anglesYaw
