# nao text to speech

import sys
from naoqi import ALProxy
import vision_definitions

IP = "nao2.local"
PORT = 9559

try:
    camProxy = ALProxy("ALVideoDevice", IP, PORT)
except Exception,e:
    print "Could not create proxy to ALVideoDevice"
    print "Error was: ",e
    sys.exit(1)

resolution = vision_definitions.kQVGA
colorSpace = vision_definitions.kYUVColorSpace
fps = 30

nameId = camProxy.subscribe("python_GVM", resolution, colorSpace, fps)
print nameId

print 'getting images in local'
for i in range(0, 20):
  camProxy.getImageLocal(nameId)
  camProxy.releaseImage(nameId)

resolution = vision_definitions.kQQVGA
camProxy.setResolution(nameId, resolution)

print 'getting images in remote'
for i in range(0, 20):
  camProxy.getImageRemote(nameId)

camProxy.unsubscribe(nameId)

print 'end of gvm_getImageLocal python script'
