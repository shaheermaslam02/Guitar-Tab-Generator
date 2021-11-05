from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import numpy
import aubio
import matplotlib.pyplot as plt
from playsound import playsound
import sounddevice as sd
import numpy as np

# using sounddevice as sd to record audio from mic for duration of 5 seconds?
def playAndRecord():
    fs=44100
    duration = 10  # seconds
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
    print("Recording Audio")
    print("Audio recording complete")
    write('output.wav', fs, myrecording)  # Save as WAV file 
    return myrecording # returning recording

def graphSong(s):
    song = AudioSegment.from_wav(s)
    # segment in milliseconds
    segment_ms = 50
    # decibels relative to maximum possible loudness
    volume = [segment.dBFS for segment in song[::segment_ms]]

    # Filter out lower frequencies to reduce noise
    #song = song.high_pass_filter(80)

    # graphing the frequencies
    x_axis = np.arange(len(volume)) * (segment_ms / 1000)
    plt.plot(x_axis, volume)
    plt.show()

# testing code and functions
def testCode():
    playAndRecord()

# recording a normal recording really quick

while (True):
    # list of commands
    commands = ['Play', 'Exit', 'Pydub']
    # taking user input
    play = input(f'Type one of the commands in {commands}: ')
    if play == 'Play':
        start = input('Enter any key to start recording!')
        songFile = playAndRecord() # calling playAndRecord() method
        print('Playing back recording...')
        sd.play(songFile, 44100)
        sd.wait()
        print('Recording finished!')
        graphSong('output.wav')
    elif play == 'Exit':
        print('Stopping program...')
        break
    elif play == 'Pydub':
        # processing song file into numpy arrays of frequencies for graphing
        path = 'FadeToBlack.wav'
        graphSong(path)

        '''trying to figure out how to play file, but not working'''

        #play(song)
        #sd.play(song, 44100)
        #sd.wait()
        #print(song)
        #playsound('FadeToBlack.wav')
        #play(song)

