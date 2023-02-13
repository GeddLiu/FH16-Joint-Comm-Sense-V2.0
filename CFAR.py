
import numpy as np
import matplotlib.pyplot as plt

# reading csv file
file = open('tone3.csv')

samples = []
for cell in file:
    if cell[0] != '-' and cell[0] != '0' and cell[0] != '1' and cell[0] != '2':
        for char in cell:
            if not char.isdigit():
                if char != '-' and char != '0' and char != '1' and char != '2' and char != '.':
                    cell = cell.replace(char, "")

    samples.append(float(cell))

file.close()

numSamples = len(samples)

fs = 1000  # sampling freq
tStep = 1 / fs  # sample time interval
f0 = 500  # sig freq

fStep = fs / numSamples
f = np.linspace(0, (numSamples - 1) * fStep, numSamples)
t = np.linspace(0, (numSamples - 1) * tStep, numSamples)

# fft

X = np.fft.fft(samples)
xMag = np.abs(X) / numSamples

fPlot = f[0:int(numSamples/2 + 1)]                  #frequency values
xMagPlot = 2 * xMag[0:int(numSamples/2 + 1)]        #power values
xMagPlot[0] = xMagPlot[0] / 2

#detect peaks
def detectPeaks(x, numTrain, numGuard, FARate):
    # Detect peaks with CFAR algorithm.
    # numTrain: # of training cells
    # numGuard: # of guard cells
    # FARate: false alarm rate

    numCells = len(x)
    numTrainHalf = round(numTrain / 2)
    numGuardHalf = round(numGuard / 2)
    numSide = numTrainHalf + numGuardHalf

    alpha = numTrain*(FARate**(-1/numTrain) - 1)    #multiplier

    peaks = []
    for i in range(numSide, numCells - numSide):

        if i != i-numSide+np.argmax(x[i-numSide:i+numSide+1]):
            continue

        sum1 = np.sum(x[i-numSide:i+numSide+1])
        sum2 = np.sum(x[i-numGuardHalf:i+numGuardHalf+1])

        pNoise = (sum1 - sum2)/numTrain
        threshold = alpha * pNoise

        if x[i] > threshold:
            peaks.append(i)

    peaks = np.array(peaks, dtype=int)

    return peaks

xMagAvg = abs(sum(samples)/len(samples))
print("average is =", xMagAvg)

numTrainCells = xMagAvg 
print("train cells is =", numTrainCells)

peakIdx = detectPeaks(samples, numTrainCell=8, numGuard=2, FARate=1e-12)

print("peaks =", peakIdx)

# plot
fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1)
ax1.plot(t, samples, '.-')
ax2.plot(fPlot, xMagPlot, '.-')

for i in peakIdx:
    ax1.plot(t[i], samples[i], 'rD')

ax1.set_xlabel("time (s)")
ax2.set_xlabel("frequency (Hz)")
ax1.grid()
ax2.grid()
plt.show()