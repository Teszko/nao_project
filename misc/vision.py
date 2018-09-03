def detect_blob(img, color, agent):
    center = -1
    if color == "red":
        center = detect_red_blob(image)
    elif color == "green":
        center = detect_green_blob(image)
    elif color == "blue":
        center = detect_blue_blob(image)

    if center != -1:
        return get_distance(center, agent)
    else:
        return -1


def detect_red_blob(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([5, 50, 50])
    upper_red = np.array([15, 255, 255])
    mask0 = cv2.inRange(img, lower_red, upper_red)
    #cv2.imshow("Mask0", mask0)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(img, lower_red, upper_red)
    #cv2.imshow("Mask1", mask1)

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

def detect_green_blob(image):
    center = -1

    return center

def detect_blue_blob(image):
    center = -1

    return center


def get_distance(center, agent):
    # get head_angles values
    anglesYaw, anglesPitch = agent.robot.get_head_angle()
    # get y and y coordinates
    x_coordinate = center[0]
    y_coordinate = center[1]

    # compute angle for points not in center of image (imagesize: 640 x 480)
    y_offset = y_coordinate + 240

    anglesYaw = anglesYaw + y_offset * (47.64 / 480)  # 47.64 degrees in x direction

    # distance = camera_height/ tan (90-head_angle)
    distance = 10

    return distance, anglesYaw