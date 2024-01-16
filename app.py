from ARPlugin import *
#Python 3.10.9
import time
time.sleep(0.05)
path = 'overlay.mp4'
mtx = np.array([[932.19753506,   0.,       675.30175538],
                 [  0.,       941.84409676, 383.48240522],
                 [  0.,           0.,           1.,        ]])

dist = np.array([[-0.12451034,  1.77519434, -0.01735062,  0.01675494, -5.34664433]])


AR = ARPlugin( mtx, dist)

AR.createCameraObj()

AR.RunPlugin_BLOCKING(path)
