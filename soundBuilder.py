import numpy as np
import wave
import struct
import matplotlib.pyplot as plt
import scipy.signal
import utils


class SoundBuilder:

    @staticmethod
    def compare(sbA, sbB):
        print(f"sbA: {sbA.numSamples} samples at {sbA.sampleRate} samples/sec")
        print(f"sbB: {sbB.numSamples} samples at {sbB.sampleRate} samples/sec")
        print(
            f"average error: {np.average(sbA.getSamples() - sbB.getSamples())}")

    @staticmethod
    def binarySamplesToFloats(samples_binary):
        samples_int16 = utils.bytesToInt16List(samples_binary)
        return samples_int16 / 32768

    @staticmethod
    def _plotNewFigure(xVector, yVector, title=None, xlabel=None, ylabel=None):
        plt.figure()
        if title != None:
            plt.title(title)
        if xlabel != None:
            plt.xlabel(xlabel)
        if ylabel != None:
            plt.ylabel(ylabel)
        plt.plot(xVector, yVector)

    @staticmethod
    def showPlots():
        plt.show()

    def __init__(self, sampleRate=None, numSamples=None, floatSamples=None, wavFile=None, rawFile=None):
        if wavFile != None:
            self.readWavFile(wavFile)
        elif rawFile != None:
            self.readRawFile(rawFile, sampleRate)
        elif floatSamples is not None:
            self.sampleRate = sampleRate
            self.samples_float = floatSamples[:]
            self.numSamples = len(self.samples_float)
        else:
            self.sampleRate = sampleRate
            self.numSamples = numSamples
            self.samples_float = np.zeros(self.numSamples)

    def getClip(self, startTime=None, endTime=None):
        startSampleIndex = 0 if startTime == None else int(
            startTime * self.sampleRate)
        endSampleIndex = self.numSamples if endTime == None else int(
            endTime*self.sampleRate)
        return SoundBuilder(
            sampleRate=self.sampleRate,
            floatSamples=self.samples_float[startSampleIndex:endSampleIndex]
        )

    def getSamples(self):
        return self.samples_float[:]

    def addSineWave(self, frequency, amplitude):
        timeVector = np.arange(self.numSamples) / self.sampleRate
        self.samples_float += amplitude * \
            np.sin(2 * np.pi * frequency * timeVector)

    def plotAmplitudeVsTime(self, titlePrefix=""):

        def getTimeAxisData(sampleRate, numSamples):
            durationSeconds = numSamples / sampleRate
            return np.linspace(0, durationSeconds, num=numSamples, endpoint=False)

        plt.figure()
        plt.title(titlePrefix)
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.plot(
            getTimeAxisData(self.sampleRate, self.numSamples),
            self.samples_float
        )

    def plotAllFFTProducts(self, titlePrefix=""):

        fftResult = self.fftShifted()
        absFFTResult = np.abs(fftResult)
        amplitudes = np.abs(fftResult / len(fftResult))
        # Positive frequencies are on right side of shifted FFT result
        amplitudesMappedToPositiveFrequencies = 2 * \
            amplitudes[len(fftResult)//2:]

        sampleIndices = np.arange(self.numSamples)
        self._plotNewFigure(
            xVector=sampleIndices,
            yVector=absFFTResult,
            title="FFT Raw Result Magnitude vs. Sample Index",
            xlabel="Sample Index",
            ylabel="Magnitude"
        )

        normalizedFrequencies = self._getNormalizedFrequencies()
        self._plotNewFigure(
            xVector=normalizedFrequencies,
            yVector=absFFTResult,
            title="FFT Raw Result Magnitude vs. Normalized Frequency (full range)",
            xlabel="Frequency",
            ylabel="Magnitude"
        )

        absoluteFrequencies = self._getAbsoluteFrequencies()
        self._plotNewFigure(
            xVector=absoluteFrequencies,
            yVector=absFFTResult,
            title="FFT Raw Result Magnitude vs. Absolute Frequency (full range)",
            xlabel="Frequency",
            ylabel="Magnitude"
        )

        absoluteFrequencies = self._getAbsoluteFrequencies()
        self._plotNewFigure(
            xVector=absoluteFrequencies,
            yVector=amplitudes,
            title="Amplitude vs. Absolute Frequency (full range)",
            xlabel="Frequency",
            ylabel="Amplitude"
        )

        positiveAbsoluteFrequencies = self._getPositiveAbsoluteFrequencies()
        self._plotNewFigure(
            xVector=positiveAbsoluteFrequencies,
            yVector=amplitudesMappedToPositiveFrequencies,
            title="Amplitude vs. Absolute Frequency",
            xlabel="Frequency",
            ylabel="Amplitude"
        )

    # The operations used to generate these products are the best I've found so far
    def plotBestFFTProducts(self, titlePrefix=""):
        fftResult = np.fft.fft(self.samples_float)

        timeVector = np.arange(self.numSamples) / self.sampleRate
        self._plotNewFigure(
            xVector=timeVector,
            yVector=self.samples_float,
            title=f"{titlePrefix}{' -- ' if len(titlePrefix) > 0 else ''}Signal Amplitude vs. Time",
            xlabel="Time (seconds)",
            ylabel="Amplitude"
        )

        frequencies = np.fft.fftfreq(self.numSamples, 1 / self.sampleRate)
        fftAmplitudes = np.abs(fftResult / len(fftResult))

        postiveFrequenciesMask = np.where(frequencies > 0)
        positiveFrequencies = frequencies[postiveFrequenciesMask]
        # Multiply positive-frequency amplitudes by 2 to show energy
        #     from symmetric negative frequencies
        adjustedAmplitudes = 2 * fftAmplitudes[postiveFrequenciesMask]

        self._plotNewFigure(
            xVector=positiveFrequencies,
            yVector=adjustedAmplitudes,
            title=f"{titlePrefix}{' -- ' if len(titlePrefix) > 0 else ''}Amplitude vs. Absolute Frequency",
            xlabel="Frequency (Hz)",
            ylabel="Amplitude"
        )

        # Why does this increase when increasing numSamples? Doesn't power measure
        #     instantaneous instensity of signal (band) rather than describing a
        #     summed quantity?
        # power = np.abs(fftResult) ** 2

        # TODO: Plot power vs. absolute frequencies

    # TODO: DRY
    def lowPassFilter(self, threshold):
        frequencies = np.fft.rfftfreq(self.numSamples, 1 / self.sampleRate)
        signalRealFFT = np.fft.rfft(self.samples_float)
        signalRealFFT[np.abs(frequencies) > threshold] = 0
        self.samples_float = np.fft.irfft(signalRealFFT)

    # TODO: DRY
    def highPassFilter(self, threshold):
        frequencies = np.fft.rfftfreq(self.numSamples, 1 / self.sampleRate)
        signalRealFFT = np.fft.rfft(self.samples_float)
        signalRealFFT[np.abs(frequencies) < threshold] = 0
        self.samples_float = np.fft.irfft(signalRealFFT)

    def bandPassFilter(self, highPassThreshold, lowPassThreshold):
        self.highPassFilter(highPassThreshold)
        self.lowPassFilter(lowPassThreshold)

    def getFrequencyPeaksFromFFT(self, magnitudeThreshold=0.001):
        fftResult = np.abs(self.fft())
        amplitudes = np.abs(fftResult / len(fftResult))
        # Positive frequencies are on left side of non-shifted FFT result
        amplitudesMappedToPositiveFrequencies = 2 * \
            amplitudes[:len(fftResult)//2]
        frequencyVector = self._getPositiveAbsoluteFrequencies()
        return [
            {
                "frequency": frequencyVector[peakIndex],
                "magnitude": amplitudesMappedToPositiveFrequencies[peakIndex]
            } for peakIndex in scipy.signal.find_peaks(amplitudesMappedToPositiveFrequencies, threshold=0.0001)[0]
        ]

    def readRawFile(self, fileName, sampleRate):
        self.sampleRate = sampleRate
        f = open(fileName, "rb")
        samples_binary = f.read()
        f.close()
        self.samples_float = self.binarySamplesToFloats(samples_binary)
        self.numSamples = len(self.samples_float)

    def readWavFile(self, fileName):
        wav = wave.open(fileName)
        self.sampleRate = wav.getframerate()
        self.numSamples = wav.getnframes()
        samples_binary = wav.readframes(self.numSamples)
        self.samples_float = self.binarySamplesToFloats(samples_binary)

    def writeWav(self, fileName):
        self._imposeMinimum(-1)
        self._imposeMaximum(1)
        wav = wave.open(fileName, 'w')
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

    def fft(self):
        return np.fft.fft(self.samples_float)

    def fftShifted(self):
        return np.fft.fftshift(np.fft.fft(self.samples_float))

    def _getNormalizedFrequencies(self):
        indicesCenteredAboutZero = np.arange(
            start=-int(self.numSamples)/2, stop=self.numSamples/2)
        return indicesCenteredAboutZero / self.numSamples

    def _getAbsoluteFrequencies(self):
        return self._getNormalizedFrequencies() * self.sampleRate

    def _getPositiveAbsoluteFrequencies(self):
        return self._getAbsoluteFrequencies()[self.numSamples // 2:]

    def _imposeMinimum(self, minimumSampleValue):
        self.samples_float = np.maximum(self.samples_float, minimumSampleValue)

    def _imposeMaximum(self, maximumSampleValue):
        self.samples_float = np.minimum(self.samples_float, maximumSampleValue)

    # TODO: Learn how to use filters
    #           https://scipy-lectures.org/intro/scipy/auto_examples/plot_fftpack.html
    #       Record something with noise in background (low or high) and filter it out
    # TODO: Experiment with wave phase
    # TODO: Plot power and any other interesting, conceptually critical representations
    #           of FFT results (energy, acceleration, etc.)
