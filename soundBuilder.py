import numpy as np
import wave
import struct
import matplotlib.pyplot as plt
import scipy.signal as signal


class SoundBuilder:

    def __init__(self, sampleRate, numSamples):
        self.sampleRate = sampleRate
        self.numSamples = numSamples
        self.samples_float = np.zeros(self.numSamples)

    def getSamples(self):
        return self.samples_float[:]

    def addSineWave(self, frequency, amplitude):
        timeVector = np.arange(self.numSamples) / self.sampleRate
        self.samples_float += amplitude * \
            np.sin(2 * np.pi * frequency * timeVector)

    def plotAmplitudeVsTime(self):

        def getTimeAxisData(sampleRate, numSamples):
            durationSeconds = numSamples / sampleRate
            return np.linspace(0, durationSeconds, num=numSamples, endpoint=False)

        plt.figure(1)
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.plot(
            getTimeAxisData(self.sampleRate, self.numSamples),
            self.samples_float
        )

    # TODO: abstract FFT result-handling here and in getFreqPeaks
    def plotFFT(self):
        fftResult = np.fft.fft(self.samples_float)
        plt.figure()
        plt.xlabel("Frequency")
        plt.ylabel("Magnitude")
        frequencyVector = self.sampleRate * \
            np.arange(self.numSamples / 2) / self.numSamples
        magnitudes = fftResult[:self.numSamples // 2] / self.numSamples
        magnitudes[1:] = 2 * magnitudes[1:]
        plt.plot(frequencyVector, np.abs(magnitudes))

    def getFrequencyPeaksFromFFT(self, magnitudeThreshold=0.001):
        fftResult = np.fft.fft(self.samples_float)
        frequencyVector = self.sampleRate * \
            np.arange(self.numSamples / 2) / self.numSamples
        magnitudes = fftResult[:self.numSamples // 2] / self.numSamples
        magnitudes[1:] = 2 * magnitudes[1:]
        magnitudes = np.abs(magnitudes)
        return [
            {
                "frequency": frequencyVector[peakIndex],
                "magnitude": magnitudes[peakIndex]
            } for peakIndex in signal.find_peaks(magnitudes)[0]
        ]

    def showPlots(self):
        plt.show()

    # TODO: Take file-name arg
    def writeWav(self):
        self.imposeMinimum(-1)
        self.imposeMaximum(1)
        wav = wave.open('test.wav', 'w')
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(self.sampleRate)

        # TODO: Put this in a function
        sineWave_int16 = np.minimum(
            np.interp(self.samples_float,
                      [-1.0, 1.0], [-32768, 32768]).astype(int),
            32767
        )

        # TODO: Do this more concisely
        for sample_int16 in sineWave_int16:
            wav.writeframesraw(struct.pack('<h', sample_int16))

        wav.close()

    def imposeMinimum(self, minimumSampleValue):
        self.samples_float = np.maximum(self.samples_float, minimumSampleValue)

    def imposeMaximum(self, maximumSampleValue):
        self.samples_float = np.minimum(self.samples_float, maximumSampleValue)
