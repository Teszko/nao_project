import time


def init_scan(agent):
    """ Turn head fully to the right to start the scan.
    """
    current_angle = agent.robot.get_head_angle()
    #agent.robot.say("current angle "+ current_angle[0])
    agent.robot.set_head_angles([-2.0, 0])
    time.sleep(3)


def scan_view_step(agent):
    """ move the head a bit to the left and take an image. if head already
        fully to the left, take an image and finish the scan.
    """
    #agent.robot.say("scan view")
    current_angle = agent.robot.get_head_angle()
    # max yaw +-2.0857
    yaw = current_angle
    pitch = 0
    if yaw >= 2:
        # agent.robot.think.opmode = "search_done"
        agent.think.num_full_scans += 1
        agent.sense.image = agent.robot.get_img()
        agent.think.finished_scan = 1
        agent.think.scanning = 0
        return
    agent.robot.set_head_angles([yaw + agent.think.head_yaw_step, pitch])
    time.sleep(0.2)
    agent.sense.image = agent.robot.get_img()
    agent.think.scanning = 0


def scan_front(agent):
    """ takes an image while looking straigt forward.
        if this is the second attempt, change the camera, then
        take the image. if this is the third, abort.
    """
    if agent.think.num_full_scans == 1:
        agent.think.switch_camera()
    if agent.think.num_full_scans == 2:
        agent.think.num_full_scans = 0
        agent.think.finished_scan = 1
        agent.think.scan_type = 0
        agent.think.scanning = 0
        return
    agent.think.finished_scan = 0
    agent.robot.say("scan front")
    agent.robot.set_head_angles([0, 0])
    time.sleep(0.5)
    agent.sense.image = agent.robot.get_img()
    agent.think.num_full_scans += 1
    agent.think.scanning = 0


def look_straight(agent):
    """makes the robot look straigt forward.
    """
    agent.robot.set_head_angles([0, 0])
    time.sleep(2)


def pose_ready(agent):
    """if the robot is sitting down, stand up. give audio feedback.
    """
    agent.sense.posestate = "ready"
    agent.robot.wake()
    time.sleep(2)
    agent.robot.initPose()
    time.sleep(2)
    agent.robot.say("ready")
    # robot say ready


def pose_rest(agent):
    """move the robot back into a resting position.
    """
    agent.sense.posestate = "rest"
    agent.robot.rest()
    time.sleep(5)
    agent.robot.say("resting")
    # robot say ready


def go_to(distance, angle):
    """make the robot turn by a specific angle and walk a specific distance.

    Args:
        distance (float): distance in meter.
        angle (float): angle in radians.
    """
    def actual_go_to(agent):
        agent.robot.go_to(distance, angle)
        # agent.think.opmode = "searching"
        agent.think.walking = 0
    return actual_go_to
    # return lambda agent: agent.robot.go_to(distance, angle)

