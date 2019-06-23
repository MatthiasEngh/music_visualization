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
  'timeInfo': None
}

# the stream stuff

def talk(**kwargs):
  global soundData
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

def run_thread():
  global soundData
  global streamRunning
  while streamRunning:
    if not soundData['read']:
      print(soundData['timeInfo'])
      soundData['read'] = True

# the running

_thread.start_new_thread(run_thread, ())
stream.start_stream()

time.sleep(3)

stream.stop_stream()
stream.close()
wf.close()

streamRunning = False

