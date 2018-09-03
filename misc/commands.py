import time


def init_scan(agent):
    current_angle = agent.robot.get_head_angle()
    agent.robot.set_head_angle([-2.08, 0])


def scan_view_step(agent):
    agent.robot.say("scan view")
    current_angle = agent.robot.get_head_angle()
    # max yaw +-2.0857
    yaw = current_angle[0]
    if yaw >= 2:
        # agent.robot.think.opmode = "search_done"
        return
    agent.robot.set_head_angle([yaw + agent.think.head_yaw_step, current_angle[1]])
    time.sleep(1)
    agent.sense.image = agent.robot.get_img()
    agent.sense.__scan_state = 0


def pose_ready(agent):
    agent.robot.say("ready")
    agent.robot.wakeUp()
    time.sleep(5)
    agent.robot.initPose()
    time.sleep(5)
    # robot say ready


def pose_rest(agent):
    agent.robot.say("resting")
    agent.robot.rest()
    time.sleep(5)
    # robot say ready


def go_to(distance, angle):
    return lambda agent: agent.robot.go_to(distance, angle)

