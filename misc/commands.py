import time


def init_scan(agent):
    agent.robot.say("init scan")
    agent.sense.scan_state = 1
    current_angle = agent.robot.get_head_angle()
    #agent.robot.say("current angle "+ current_angle[0])
    agent.robot.set_head_angles([-2.0, 0])
    time.sleep(3)
    agent.sense.scan_state = 0


def scan_view_step(agent):
    agent.robot.say("scan view")
    current_angle = agent.robot.get_head_angle()
    # max yaw +-2.0857
    yaw = current_angle
    pitch = 0
    if yaw >= 2:
        # agent.robot.think.opmode = "search_done"
        return
    agent.robot.set_head_angles([yaw + agent.think.head_yaw_step, pitch])
    time.sleep(0.2)
    agent.sense.image = agent.robot.get_img()
    agent.sense.scan_state = 0


def scan_front(agent):
    agent.robot.say("scan front")
    agent.robot.set_head_angles([0, 0])
    time.sleep(0.2)
    agent.sense.image = agent.robot.get_img()
    agent.sense.scan_state = 0


def look_straight(agent):
    agent.robot.set_head_angles([0, 0])
    time.sleep(2)


def pose_ready(agent):
    agent.sense.posestate = "ready"
    agent.robot.wake()
    time.sleep(2)
    agent.robot.initPose()
    time.sleep(2)
    agent.robot.say("ready")
    # robot say ready


def pose_rest(agent):
    agent.robot.rest()
    time.sleep(5)
    agent.robot.say("resting")
    # robot say ready


def go_to(distance, angle):
    def actual_go_to(agent):
        agent.robot.go_to(distance, angle)
        agent.think.opmode = "searching"
    return actual_go_to
    # return lambda agent: agent.robot.go_to(distance, angle)

