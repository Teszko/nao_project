import sys
sys.path.insert(0, '../misc/')
from commandqueue import CommandQueue
import time

queue = CommandQueue(None)


def testQueue(agent):
    print "start test 2s"
    time.sleep(10)
    print "end test 2s"


queue.add_element(testQueue)
queue.add_element(testQueue)
queue.add_element(testQueue)


while(True):
    print "tick"
    queue.tick()
    time.sleep(0.5)
