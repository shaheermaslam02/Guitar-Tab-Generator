# Audio Processing file with methods and libraries for processing audio
import aubio
import numpy as np
import sounddevice as sd
import pyaudio
from scipy.io.wavfile import write
import time

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
    buffer_size = 2048
    channel = 1
    format = pyaudio.paFloat32
    method = "default"
    sample_rate = 44100
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
    # initializing Aubio's note detection object
    nDetection = aubio.notes(method, buffer_size,
        hop_size, sample_rate)
    # initializing Aubio's tempo detection object
    tDetection = aubio.tempo(method, buffer_size,
        hop_size, sample_rate)
    # Set unit.
    pDetection.set_unit("Hz")
    # Frequency under -40 dB will considered
    # as a silence.
    pDetection.set_silence(-40)

    return (mic, pDetection, nDetection, tDetection, hop_size)

# pitchInRealTime function to detect pitch, volume, note, tempo over time
def pitchInRealTime(mic, pDetection, nDetection, tDetection, hop_size, beforeTime):

    # mic listening
    data = mic.read(hop_size)
    # Convert into number that Aubio understand.
    samples = np.fromstring(data,
            dtype=aubio.float_type)
    # Finally get the pitch.
    pitch = pDetection(samples)[0]
    afterTime = (time.time() - beforeTime)
    # get note (FAILING)
    note = nDetection(samples)[0]
    # get Tempo
    tempo = tDetection(samples)[0]
    # Compute the energy (volume)
    # of the current frame.
    volume = np.sum(samples**2)/len(samples)
    # format output
    # display 6 decimal digits like 0.000000.
    volume = "{:6f}".format(volume)

    # print loudness value and pitch value
    print('Pitch:', str(pitch), 'Volume:', str(volume), 'Time:', str(afterTime),
            'Note:', str(note), 'Tempo:', str(tempo))
