import AudioProcessing as ap
import time

# testing if recording and saving file works (it does!)
'''
recording = ap.recordAudio()
ap.saveFile(recording, 1)
'''

wrapper = ap.pitchInRealTimeWrapper()
beforeTime = time.time()
while True:
    ap.pitchInRealTime(wrapper[0], wrapper[1], wrapper[2],
                       wrapper[3], wrapper[4], beforeTime)