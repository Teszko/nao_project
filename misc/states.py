import commands
import vision
import numpy as np


def state_wait_fn(agent):
    """ defines logic for state 'wait'"""
    speech = agent.speechQueue.pop_element()
    if speech:
        agent.sense.target = speech
        #agent.robot.say("set opmode to searching")
        agent.think.opmode = "searching"
        agent.stateMachine.change_state(agent.stateMachine.state_search, "search")


def state_done_fn(agent):
    """ defines logic for state 'done'"""
    if agent.sense.posestate != "rest":
        #agent.robot.say("done")
        agent.sense.posestate = "rest"
        agent.commandQueue.add_element(commands.pose_rest)
        agent.commandQueue.set_lock()


def state_search_fn(agent):
    """ defines logic for state 'search'"""
    if agent.sense.posestate == "rest":
        agent.commandQueue.add_element(commands.pose_ready, "pose ready")
        agent.think.init_scan()

    img = agent.sense.image
    if img is not None:
        distance, angle = vision.detect_blob(agent, agent.think.camera)
        if distance == -1:
            # handle not found
            if agent.think.found and agent.think.finished_scan:
                agent.think.found = 0
        else:
            agent.think.num_full_scans = 0
            agent.think.found = 1
            agent.think.scan_type = 1
            #agent.robot.say("distance " + str(np.around(distance, 1)))
            distance = min(agent.think.max_dist, distance)
            agent.think.walk_to_target(distance, angle)
            if distance < 0.4:
                agent.stateMachine.change_state(agent.stateMachine.state_done, "done")
                # end condition

        agent.sense.image = None
        return

    if agent.think.walking:
        return

    if agent.think.scanning:
        return

    if agent.think.scan_type == 1:
        agent.think.scanning = 1
        agent.commandQueue.add_element(commands.scan_front, "scan front")
        return

    if agent.think.scan_type == 0 and not agent.think.finished_scan:
        agent.think.scanning = 1
        agent.commandQueue.add_element(commands.scan_view_step, "scan view b")
        return

    if agent.think.scan_type == 0 and agent.think.finished_scan:
        if agent.think.num_full_scans > 2:
            #agent.robot.say("too many scans failed.")
            agent.stateMachine.change_state(agent.stateMachine.state_done, "done")
        else:
            agent.think.switch_camera()
            agent.think.init_scan()


class StateMachine:
    """ governs which state the robot is in. wait, search, done """
    def __init__(self, agent):
        self.agent = agent
        self.type = "wait"
        self.current_state = None
        self.state_wait = state_wait_fn
        self.state_search = state_search_fn
        self.state_done = state_done_fn
        self.current_state = self.state_wait

    def change_state(self, state, type):
        """ change current state to different state """
        self.current_state = state
        self.type = type

    def tick(self):
        """ run current state """
        if self.current_state is not None:
            self.current_state(self.agent)
