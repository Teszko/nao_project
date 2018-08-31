from __future__ import print_function

import socket
import time
import struct

robotIp = "127.0.0.1"
robotPort = 3100

class Robot(object):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 sync_mode=True):
        self.sync_mode = sync_mode
        self.connect(simspark_ip, simspark_port)
        self.send_command('(scene rsg/agent/naov4/nao.rsg)')

        init_cmd = ('(init (unum ' + str(0) + ')(teamname ' + "noteam" + '))')
        self.send_command(init_cmd)

    def connect(self, simspark_ip, simspark_port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((simspark_ip, simspark_port))

    def send_command(self, commands):
        if self.sync_mode:
            commands += '(syn)'
        self.socket.sendall(struct.pack("!I", len(commands)) + commands)

if __name__ == "__main__":
    agent = Robot()
    while (1):
        print(".", end="")
        agent.send_command('')