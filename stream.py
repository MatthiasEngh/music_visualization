import _thread
import matplotlib.pyplot as plt
import numpy
import pyaudio
import struct
import sys
import time
import wave

wf = wave.open("seriously.wav", "rb")
pyAudioInstance = pyaudio.PyAudio()

soundData = {
  'read': True,
  'timeInfo': {},
  'rawData': []
}

audioFormat = pyAudioInstance.get_format_from_width(wf.getsampwidth())
channels = wf.getnchannels()
frameRate = wf.getframerate()


print("format: ", audioFormat)
print("channels: ", channels)
print("frame rate: ", frameRate)

# the stream stuff

def talk(**kwargs):
  global soundData
  soundData['frameCount'] = kwargs['frameCount']
  soundData['rawData'] = kwargs['rawData']
  soundData['read'] = False
  soundData['timeInfo'] = kwargs['timeInfo']

def next_frame(in_data, frame_count, time_info, status):
  data = wf.readframes(frame_count)
  talk(rawData = data, timeInfo = time_info, frameCount = frame_count)
  return (data, pyaudio.paContinue)

stream = pyAudioInstance.open(
  format=pyAudioInstance.get_format_from_width(wf.getsampwidth()),
  channels=wf.getnchannels(),
  rate=wf.getframerate(),
  output=True,
  stream_callback=next_frame
)

# the draw stuff

streamRunning = True

hasPrint = False

fig, ax = plt.subplots()

def visualize(frameCount, rawData):
  global hasPrint
  data = struct.unpack("<%dh" % (2 * frameCount), rawData)
  values = numpy.array(data)
  values.shape = (frameCount, 2)
  channels = numpy.transpose(values)
  ax.clear()
  ax.plot(channels[0])
  ax.plot(channels[1])
  ax.set_ylim(-15000, 15000)
  plt.pause(0.01)

def run_thread():
  global soundData
  global streamRunning
  while streamRunning:
    if not soundData['read']:
      visualize(soundData['frameCount'], soundData['rawData'])
      soundData['read'] = True

# the running

stream.start_stream()
run_thread()

time.sleep(3)

stream.stop_stream()
stream.close()
wf.close()

streamRunning = False

