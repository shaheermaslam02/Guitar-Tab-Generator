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
while i <= 100:
    temp = ap.fakePitchInRealTime(wrapper[0], wrapper[1], wrapper[2],
                       wrapper[3], wrapper[4], beforeTime)
    print(temp[6])
    #print('Samples: ', temp[5])

    # using zero crossing rate algorithm
    '''
    frequency = ap.zeroCrossingRate(temp[5])
    print('Frequency: ', frequency)
    '''

    auto = ap.AutoCorrelation(temp[5])
    original += list(temp[5])
    autocorrelation += auto[0]
    #frequency = ap.zeroCrossingRate(auto[0])
    #print('Frequency: ', frequency)
    i += 1
j = 0
#print('Autocorrelation: ', autocorrelation)

lags = [l for l in range(len(autocorrelation))]

# autocorrelated graph, less noise
plt.plot(lags, autocorrelation)
plt.title('Autocorrelation Graph')
plt.show()
# original graph of samples
plt.plot(lags, original)
plt.title('Original Sample Graph')
plt.show()

frequencies = []
while j < len(autocorrelation) / 1024:  
    frequency = ap.zeroCrossingRate(autocorrelation[j * 1024 : (j + 1) * 1024])
    print('Frequency: ', frequency)
    frequencies.append(frequency)
    j += 1

#print(frequencies)
