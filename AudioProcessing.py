# Audio Processing file with methods and libraries for processing audio

# audio libraries
import aubio
import sounddevice as sd
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

# E2 is the baseline, D#6 is last note
# first in tuple is string 0-5, second is fret 0-23
standard_guitar_dict = {'E2' : {(0, 0)}, 'F2' : {(0, 1)}, 'F#2/Gb2' : {(0, 2)},
                        'G2' : {(0, 3)}, 'G#2/Ab2' : {(0, 4)}, 'A2' : {(0, 5), (1, 0)},
                        'A#2/Bb2' : {(0, 6), (1, 1)}, 'B2' : {(0, 7), (1, 2)}, 'C3' : {(0, 8), (1, 3)},
                        'C#3/Db3' : {(0, 9), (1, 4)}, 'D3' : {(0, 10), (1, 5), (2, 0)}, 'D#3/Eb3' : {(0, 11), (1, 6), (2, 1)},
                        'E3' : {(0, 12), (1, 7), (2, 2)}, 'F3' : {(0, 13), (1, 8), (2, 3)}, 'F#3/Gb3' : {(0, 14), (1, 9), (2, 4)},
                        'G3' : {(0, 15), (1, 10), (2, 5), (3, 0)}, 'G#3/Ab3' : {(0, 16), (1, 11), (2, 6), (3, 1)}, 'A3' : {(0, 17), (1, 12), (2, 7), (3, 2)},
                        'A#3/Bb3' : {(0, 18), (1, 13), (2, 8), (3, 3)}, 'B3' : {(0, 19), (1, 14), (2, 9), (3, 4), (4, 0)}, 'C4' : {(0, 20), (1, 15), (2, 10), (3, 5), (4, 1)},
                        'C#4/Db4' : {(0, 21), (1, 15), (2, 10), (3, 6), (4, 2)}, 'D4' : {(0, 22), (1, 16), (2, 11), (3, 7), (4, 3)}, 'D#4/Eb4' : {(0, 23), (1, 17), (2, 12), (3, 8), (4, 4)},
                        'E4' : {(0, 24), (1, 18), (2, 13), (3, 9), (4, 5), (5, 0)}, 'F4' : {(1, 19), (2, 14), (3, 10), (4, 6), (5, 1)}, 'F#4/Gb4' : {(1, 20), (2, 15), (3, 11), (4, 7), (5, 2)},
                        'G4' : {(1, 21), (2, 16), (3, 12), (4, 8), (5, 3)}, 'G#4/Ab4' : {(1, 22), (2, 17), (3, 13), (4, 9), (5, 4)}, 'A4' : {(1, 23), (2, 18), (3, 14), (4, 10), (5, 5)},
                        'A#4/Bb4' : {(1, 24), (2, 19), (3, 15), (4, 11), (5, 6)}, 'B4' : {(2, 20), (3, 16), (4, 12), (5, 7)}, 'C5' : {(2, 21), (3, 17), (4, 13), (5, 8)},
                        'C#5/Db5' : {(2, 22), (3, 18), (4, 14), (5, 9)}, 'D5' : {(2, 23), (3, 19), (4, 15), (5, 10)}, 'D#5/Eb5' : {(2, 24), (3, 20), (4, 16), (5, 11)},
                        'E5' : {(3, 21), (4, 17), (5, 12)}, 'F5' : {(3, 22), (4, 18), (5, 13)}, 'F#5/Gb5' : {(3, 23), (4, 19), (5, 14)}, 'G5' : {(3, 24), (4, 20), (5, 15)},
                        'G#5/Ab5' : {(4, 21), (5, 15)}, 'A5' : {(4, 22), (5, 16)}, 'A#5/Bb5' : {(4, 23), (5, 17)}, 'B5' : {(4, 24), (5, 18)}, 'C6' : {(5, 19)}, 
                        'C#6/Db6' : {(5, 20)}, 'D6' : {(5, 21)}, 'D#6/Eb6' : {(5, 22)}, 'E6' : {(5, 23)}, 'F3' : {(5, 24)}}

# set of fret numbers
frets = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
         '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'}

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

# pitchInRealTimeWrapper function for parameters to pitchInRealTime
def pitchInRealTimeWrapper():
    # initiating variables for use in sampling, tracking audio, etc.

    # buffer_size: amount of time allowed for computer to process audio from mic, 2048 samples
    buffer_size = 2048
    # channel: simply recording through one channel (one microphone)
    channel = 1
    # format for pyaudio.paFloat32 type
    format = pyaudio.paFloat32
    # default method
    method = "default"
    # number of times audio is captured per second, standard is 44.1 kHz
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
    # under -40 Hz considered silence
    pDetection.set_silence(-40)

    return (mic, pDetection, tDetection, oDetection, hop_size)

# reference for pitch detection: 
# https://stackoverflow.com/questions/66508539/how-would-i-retrieve-the-pitch-and-loudness-from-other-samples-of-the-microphone 

# pitchInRealTime function to detect pitch, volume, note, tempo over time
def pitchInRealTime(mic, pDetection, tDetection, oDetection, hop_size, beforeTime):
    # mic listening
    data = mic.read(hop_size)
    # convert to aubio.float_type
    samples = np.fromstring(data,
            dtype=aubio.float_type)
    # getting onset
    onset = oDetection(samples)[0]
    # getting the pitch
    pitch = pDetection(samples)[0]
    # getting time when reading pitch
    afterTime = (time.time() - beforeTime)
    # formatting with 6 decimal places
    afterTime = "{:6f}".format(afterTime)
    # using helper function with note dictionary to convert pitch to note
    note = pitchToNote(pitch)
    # get tempo
    tempo = tDetection(samples)[0]
    # getting volume by root mean square, which measures output: 
    volume = math.sqrt(np.sum(samples**2)/len(samples))
    # format output with 6 decimel places
    volume = "{:6f}".format(volume)
    pitchFreq = ''
    # determining whether the pitch is low, mid or high
    if 0 <= pitch <= 140:
        pitchFreq = 'Low'
    elif 140 < pitch <= 2000:
        pitchFreq = 'Mid'
    elif pitch > 2000:
        pitchFreq = 'High'
    # print loudness value and pitch value
    '''
    print(pitchFreq + ' Pitch:', str(pitch), 'Volume:', str(volume), 
          'Time:', str(afterTime), 'Note:', str(note))
    '''
    return(pitch, volume, afterTime, note, tempo)

# pitchToNote function to find the note of a pitch within a
# range of .45 Hz
def pitchToNote(pitch, notes = note_dictionary):
    for i in notes:
        temp = notes[i][0]
        # selected 2 since base note in standard tuning E2 difference with
        # next note is around 4.9, so to keep notes distinct based on distance,
        # checking within 2 as distance between note frequencies gets larger
        # the higher you go
        if temp - 2 <= pitch <= temp + 2 and pitch > 76:
            return i
    return None

# volume difference function

def volumeDifference(current, last):
    if float(current[1]) - float(last[1]) >= 0.1:
        return True
    return False        
 
def miniTabDissection(section):
    note = section[0][3]
    for i in section[1:]:
        if i[3] != note:
            return False
    return True

# getting tuple (string, fret) for the note
def getTab(note):
    tab = standard_guitar_dict.get(note, {})
    if tab != {}:
        stringFret = ''
        for i in tab:
            if stringFret == '':
                stringFret = i
            elif i[1] < stringFret[1]:
                stringFret = i
        if stringFret == '':
            return None
        else:
            return stringFret
    return None

# tab dissection function to correctly store notes into guitar tab
def tabDissection(notes):
    newTab = []
    lastNote = ''
    lastTabbed = ''
    index = 0
    for i in notes:
        if float(i[1]) >= 0.1:
            lastNote = i
            break
        index += 1
    count = 1
    fakeIndex = index + 1
    print('First Note: ', lastNote[3])
    for i in notes[index + 1:]:
        print(count)
        if i[3] == lastNote[3]:
            count += 1
        elif volumeDifference(i, notes[fakeIndex - 1]):
            if count >= 5:
                tab = getTab(lastNote[3])
                if lastTabbed == '':
                    lastTabbed = lastNote[4]
                elif i[4] <= lastTabbed:
                    lastTabbed = lastNote[4] + 2
                else:
                    lastTabbed = i[4]
                newTab.append((tab[0], tab[1], lastTabbed))
                lastNote = i
                print('New note:', lastNote[3])
                count = 1
            else:
                lastNote = i
                print('New Note:', lastNote[3])
                count = 1
        elif miniTabDissection(notes[fakeIndex : fakeIndex + 5]):
            if count >= 5:
                tab = getTab(lastNote[3])
                if lastTabbed == '':
                    lastTabbed = lastNote[4]
                elif i[4] > lastTabbed:
                    lastTabbed = i[4]
                else:
                    lastTabbed = lastTabbed + 2
                newTab.append((tab[0], tab[1], lastTabbed))
                lastNote = i
                print('New note:', lastNote[3])
                count = 1
            else:
                lastNote = i
                print('New Note:', lastNote[3])
                count = 1
        '''       
        else:
            if count >= 5:
                tab = getTab(lastNote[3])
                if lastTabbed == '':
                    lastTabbed = lastNote[4]
                elif lastTabbed <= i[4]:
                    lastTabbed = lastNote[4] + 2
                newTab.add((tab[0], tab[1], lastTabbed))
                count = 0
            lastNote = i
        '''
        fakeIndex += 1
    print(newTab)
    return newTab

# storing the tab in the positions of the guitar tab
def storeTab(notes, tab):
    for i in notes:
        tab[i[0]][i[2]] = str(i[1])
    

# notes
'''
  - minimum volume for a note should be 0.5: suggest users to use a microphone and make
    sure audio measure is loud
  - .01 volume difference required and notes stored based on time change
  - create 2D guitar list to store notes
  - fix MVC violation bug
  - if a lower string is highlighted, don't put in the higher ones into the tab
  - feature to select tempo? baseline is 120 BPM which is half a beat a second, so based on 120/input bpm,
    then 0.5 seconds / (120/input bpm), makes it easier to measure how many times to take in a note
'''