# Audio Processing file with methods and libraries for processing audio

# audio libraries
import aubio
import sounddevice as sd
import audioop
import pyaudio
from scipy.io.wavfile import write
# data breakdown and analysis libraries
import numpy as np
import pandas as pd
# miscellaneous libraries
import math
import time
import requests

# using pandas to get notes from table from a site (https://stackoverflow.com/questions/10556048/how-to-extract-tables-from-websites-in-python)
url = 'https://pages.mtu.edu/~suits/notefreqs.html'
html = requests.get(url).content
notes = pd.read_html(html)
notes = notes[-1]
# creating note dictionary using pandas iteration which maps notes to frequency
# and wavelength
note_dictionary = {notes.iloc[i, 0] : (notes.iloc[i, 1], notes.iloc[i, 2]) for i in range(len(notes))}
guitar_tab_dictionary = {}
# E2 is the baseline

# recordAudio function to record audio as a file
def recordAudio():
    fs=44100
    duration = 1000  # seconds
    myrecording = sd.rec(duration * fs,samplerate=fs, channels=1,dtype='float64')
    print('Recording Audio.')
    return myrecording # returning recording

# saveFile function to save file in folder
def saveFile(audio, count = 1):
    write('audio' + str(count) + '.wav', 44100, audio)  # Save as WAV file

# playAudio function to play file
def playAudio(audio):
    sd.play(audio, 44100)

# pitchInRealTimeWrapper function for parameters to 
def pitchInRealTimeWrapper():
    # initiating variables for use in sampling, tracking audio, etc.

    # buffer_size: amount of time allowed for computer to process audio from mic
    buffer_size = 2048
    # channel: simply recording through one channel (one microphone)
    channel = 1
    # format for pyaudio.paFloat32 type
    format = pyaudio.paFloat32
    # default method, could be 
    method = "default"
    # number of times audio is captured per second
    sample_rate = 44100
    # number of samples between frames
    hop_size = buffer_size//2

    # initializing pyAudio object
    pA = pyaudio.PyAudio()

    # opening microphone stream
    mic = pA.open(format=format, channels=channel,
        rate=sample_rate, input=True,
        frames_per_buffer=hop_size)

    # Initiating Aubio's pitch detection object.
    pDetection = aubio.pitch(method, buffer_size,
        hop_size, sample_rate)
    # initializing Aubio's tempo detection object
    tDetection = aubio.tempo(method, buffer_size,
        hop_size, sample_rate)
    # initializing Aubio's onset detection object
    oDetection = aubio.onset(method, buffer_size,
        hop_size, sample_rate)
    # setting unit in Hz
    pDetection.set_unit("Hz")
    # Frequency under -40 dB will considered
    # as a silence.
    pDetection.set_silence(-40)

    return (mic, pDetection, tDetection, oDetection, hop_size)

# pitchInRealTime function to detect pitch, volume, note, tempo over time
def pitchInRealTime(mic, pDetection, tDetection, oDetection, hop_size, beforeTime):
    # mic listening
    data = mic.read(hop_size)
    # convert to aubio.float_type
    samples = np.fromstring(data,
            dtype=aubio.float_type)
    # getting onset
    onset = oDetection(samples)[0]
    # Finally get the pitch.
    pitch = pDetection(samples)[0]
    afterTime = (time.time() - beforeTime)
    afterTime = "{:6f}".format(afterTime)
    '''
    # get note (FAILING)
    note = nDetection(samples)[0]
    '''
    note = pitchToNote(pitch)
    # get Tempo
    tempo = tDetection(samples)[0]
    '''
    still trying to get volume to work, been researching but can't figure it out
    '''
    # getting volume by root mean square
    volume = audioop.rms(samples, 1)
    # format output with 6 decimel places
    volume = "{:6f}".format(volume)

    #print(samples)

    # print loudness value and pitch value
    print('Pitch:', str(pitch), 'Volume:', str(volume), 
          'Time:', str(afterTime), 'Note:', str(note), 'Tempo:', str(tempo))
    return(pitch, volume, afterTime, note, tempo)

# pitchToNote function to find the note of a pitch within a
# range of .45 Hz
def pitchToNote(pitch, notes = note_dictionary):
    for i in notes:
        temp = notes[i][0]
        if temp - .45 <= pitch <= temp + .45:
            return i
    return None

