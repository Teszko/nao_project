import cv2
import numpy as np
import random

def detect_blob(agent, camera):
    """ Detects dot in the given image of the color specified in agent.sense.target.

        Args:
             agent: object
             camera: Id in int

        Returns: Distance to dot
    """

    center = -1
    image = agent.sense.image
    color = agent.sense.target

    #print("camera: " ,camera)
    center = get_blob_center(image, color, camera)


    if center != -1:
        return get_distance(center, agent, camera)
    else:
        return -1, None


def get_blob_center(image, color, camera):
    """ Computes the center of the dot for a picture from camera 0.
        Metric to detect ellipses: Area of the enclosing ellipse minus area of the contour in ratio to the contour area.

        Args:
            image: Image from camera
            boundaries: Boundaries for the specified color for cv2.inrange

        Returns:
              center: X/Y coordinates of center of dot
    """

    # color values in RGB
    boundaries_red = [([0, 10, 10], [15, 255, 255])]#,
                      #([170, 50, 50], [180, 255, 255])]

    #boundaries_blue = ([90, 50, 50], [120, 255, 255])
    boundaries_blue = ([100, 10, 10], [180, 255, 255])


    mask = 0
    img = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)

    if camera == 0:
        #delete noise in the upper part of the image for the top camera
        overlay = np.zeros((160, 640, 3), np.uint8)
        img[:overlay.shape[0], :overlay.shape[1]] = overlay

    #get the contours of the right color
    if color == "red":
        for (lower, upper) in boundaries_red:
            lower_boundary = np.array(lower)
            upper_boundary = np.array(upper)

            mask = mask + cv2.inRange(img, lower_boundary, upper_boundary)
            
    if color == "blue":
        lower_boundary = np.array(boundaries_blue[0])
        upper_boundary = np.array(boundaries_blue[1])

        mask = cv2.inRange(img, lower_boundary, upper_boundary)



    _, cnts, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if camera == 0:
        # area1 and area2 are the range of contour area
        area1 = 250
        area2 = 5000
        diff_best = area2 + 1
        max_diff = 4.5
        max_ellipse_stretch = 5
        best_ellipse = None
        center = -1

        #iterate through the contours
        for cnt in cnts:
            if area1 < cv2.contourArea(cnt) < area2:
                temp_ellipse = cv2.fitEllipse(cnt)
                (x, y), (MA, ma), angle = temp_ellipse
                # compute metrics
                area_ellipse = (np.pi * MA * ma)
                area_cnt = cv2.contourArea(cnt)
                diff = ((area_ellipse - cv2.contourArea(cnt)) / area_cnt)
                if min(MA, ma) != 0:
                    ellipse_stretch = (max(MA, ma) / min(MA, ma))
                else:
                    ellipse_stretch = max_ellipse_stretch + 1
                #check metrics
                if diff < diff_best and ellipse_stretch < max_ellipse_stretch and diff < max_diff:
                    diff_best = diff
                    best_ellipse = temp_ellipse

        if best_ellipse is not None:
            (x, y), (MA, ma), angle = best_ellipse
            center = (int(x), int(y))
            cv2.circle(img, center, 1, (0, 255, 0), thickness=1, lineType=8, shift=0)
            cv2.ellipse(img, best_ellipse, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow('ellipse', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            cv2.imwrite("pic_found"+str(random.randint(0,1000))+".png", image)

            print("center:", center)
        else:
            cv2.imwrite("pic_not_found"+str(random.randint(0,1000))+".png", image)

            print("no dots found!")


    else: #camera == 1
        # area1 and area2 are the range of contour area
        area1 = 200
        area2 = 200000
        max_cnt = None
        max_area = 0
        center = -1

        # iterate through the contours
        for cnt in cnts:
            if area1 < cv2.contourArea(cnt) < area2:
                if cv2.contourArea(cnt) > max_area:
                    max_cnt = cnt
                    max_area = cv2.contourArea(cnt)

        if max_cnt is not None:
            ((x, y), radius) = cv2.minEnclosingCircle(max_cnt)
            center = (int(x), int(y))
            cv2.circle(img, center, int(radius), (0, 255, 0), thickness=1, lineType=8, shift=0)
            cv2.imshow('circle', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            cv2.imwrite("pic_found" + str(random.randint(0, 1000)) + ".png", image)

            print("center:", center)
        else:
            cv2.imwrite("pic_not_found" + str(random.randint(0, 1000)) + ".png", image)

            print("no dots found!")

    #cv2.imwrite("pic"+str(random.randint(0,1000))+".png", image)
    return center



def get_distance(center, agent, camera):
    """ computes the distance to the center of the dot

        Args:
            center: Center of the dot
            agent: Object
            camera: Id in int

        Returns:
            distance: Distance to the center of the dot
            anglesYaw: Angle of the head horizontal direction
    """

    print("camera ", camera)
    # get head_angles values
    anglesYaw = agent.robot.get_head_angle()
    # get y and y coordinates
    x_coordinate, y_coordinate = center

    # compute angle for points not in center of image (imagesize: 640 x 480)
    x_offset = 320 - x_coordinate


    anglesYaw = anglesYaw + ((x_offset * (60.97/ 640)) / 360 * 2 * 3.1415)  # 47.64 degrees in x direction

    if camera == 0:
        distance = float(480 - y_coordinate) * 2.5 / 240 + 0.85
    elif camera == 1:
        distance = float(480 - y_coordinate) * 0.46 / 240 #+ 0.22
    else:
        distance = -1

    print("distance: ", distance)
    if distance > 0.5:
        distance = 0.5


    return distance, anglesYaw
