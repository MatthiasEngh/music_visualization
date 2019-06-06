import scipy.io.wavfile
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import time

rate, data = scipy.io.wavfile.read("seriously.wav")

framerate = 10
samplesize = int(rate/framerate)
adjustment = 0.1918
refreshtime = (1/framerate)*adjustment
samplesize2 = 100
stepsize = int(samplesize/samplesize2)

stereo_data = np.transpose(data)
data0 = stereo_data[0]
data1 = stereo_data[1]

soundlines0 = []
soundlines1 = []

maxlen = min([len(data0), len(data1)])
finalsampleind = maxlen - 1
firstsampleind = 0
while firstsampleind < maxlen:
  lastsampleind = min(firstsampleind + samplesize, finalsampleind)
  newsoundline0 = data0[firstsampleind:lastsampleind:stepsize]
  newsoundline1 = data1[firstsampleind:lastsampleind:stepsize]
  soundlines0.append(newsoundline0)
  soundlines1.append(newsoundline1)
  firstsampleind = lastsampleind + 1

fig, ax = plt.subplots()
plt.pause(0.1)
soundlineslength = len(soundlines0)

music = subprocess.Popen(["afplay", "seriously.wav"])

for i in range(soundlineslength):
  soundline0 = soundlines0[i]
  soundline1 = soundlines1[i]
  ax.plot(soundline0)
  ax.plot(soundline1)
  ax.set_ylim(-15000,15000)
  plt.pause(refreshtime)
  ax.clear()

time.sleep(5)
music.terminate()

