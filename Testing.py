import AudioProcessing as ap
import time
import matplotlib.pyplot as plt

# testing if recording and saving file works (it does!)
'''
recording = ap.recordAudio()
ap.saveFile(recording, 1)
'''

wrapper = ap.pitchInRealTimeWrapper()
beforeTime = time.time()
i = 0
autocorrelation = []
original = []
while i <= 50:
    temp = ap.pitchInRealTime(wrapper[0], wrapper[1], wrapper[2],
                       wrapper[3], wrapper[4], beforeTime)
    #print('Samples: ', temp[5])

    # using zero crossing rate algorithm
    '''
    frequency = ap.zeroCrossingRate(temp[5])
    print('Frequency: ', frequency)
    '''

    auto = ap.AutoCorrelation(temp[5])
    original += list(temp[5])
    autocorrelation += auto
    #frequency = ap.zeroCrossingRate(auto[0])
    #print('Frequency: ', frequency)
    i += 1
j = 0
#print('Autocorrelation: ', autocorrelation)

lags = [l for l in range(len(autocorrelation))]

peaks, indexes = ap.peakFinder(autocorrelation)

frequencies = []
frequencyIndexes = []
while j < len(autocorrelation) / 1024:  
    frequency = ap.zeroCrossingRate(autocorrelation[j * 1024 : (j + 1) * 1024])
    print('Frequency: ', frequency)
    frequencies.append(frequency)
    index = ((j + 1)*1024)
    frequencyIndexes.append(index)
    j += 1

noteIndexes = []
notes = []
plotNotes = []
for i in range(2, len(frequencies)):
    if ap.pitchToNote(frequencies[i]) != None:
        notes.append(ap.pitchToNote(frequencies[i]))
        plotNotes.append(frequencies[i] / 10)
        noteIndexes.append(frequencyIndexes[i])


print(len(frequencies))
print(len(peaks))
print(len(notes))
print(len(autocorrelation))
print(len(original))
print(notes)
print(noteIndexes)
print(indexes)

fakeFrequencies = [i / 10 for i in frequencies[2:]]

# graphing everything
fig, ax = plt.subplots(figsize = (16, 10))
ax.plot(lags, original, alpha = 0.3)
ax.plot(lags, autocorrelation, alpha = 0.5)
ax.plot(indexes, peaks)
ax.plot(frequencyIndexes[2:], fakeFrequencies)
#ax.plot(frequencyIndexes, frequencies)
ax.plot(noteIndexes, plotNotes)
ax.set_title('Autocorrelated Samples, Original and Highlighted Peaks')
ax.legend(['Original', 'Autocorrelated', 'Peaks', 'Fake Frequencies', 'Detected Notes', 'Fake AC'])
ax.grid()
plt.show()

# plt.plot([i for i in range(len(frequencies))], frequencies)
# plt.title('Frequencies Graph')
# plt.show()

'''
match peak to bin that frequency comes from, so the peaks and frequencies line up, then 
put into guitar tab storing algorithm and dissect based on whether the note is really a note or not?
'''