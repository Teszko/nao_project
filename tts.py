# nao text to speech

import sys
from naoqi import ALProxy

IP = "nao3.local"
PORT = 9559
if (len(sys.argv) > 2):
    PORT = sys.argv[2]
try:
    tts = ALProxy("ALTextToSpeech", IP, PORT)
except Exception,e:
    print "Could not create proxy to ALTextToSpeech"
    print "Error was: ",e
    sys.exit(1)

tts.say("Whaddap")
