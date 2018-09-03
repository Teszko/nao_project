import time


def init_scan(agent):
    current_angle = agent.robot.get_head_angle()
    agent.robot.set_head_angle([-2.08, 0])


def scan_view_step(agent):
    agent.think.scan_state = "progress"
    current_angle = agent.robot.get_head_angle()
    # max yaw +-2.0857
    yaw = current_angle[0]
    agent.robot.set_head_angle([yaw + agent.think.head_yaw_step, current_angle[1]])
    agent.sense.image = agent.robot.get_img()
    agent.think.scan_state = "done"


def pose_ready(agent):
    agent.robot.wakeUp()
    time.sleep(5)
    agent.robot.initPose()
    time.sleep(5)
    # robot say ready


def pose_rest(agent):
    agent.robot.rest()
    time.sleep(5)
    # robot say ready
