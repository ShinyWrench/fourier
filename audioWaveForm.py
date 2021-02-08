from sampleArray import SampleArray
import utils


class AudioWaveForm:

    def __init__(self, sampleRate, numSamples):
        self.sampleRate = sampleRate
        self.numSamples = numSamples
        self.sampleArrayNormalized = SampleArray(numSamples=self.numSamples)

    def addSineWave(self, frequency, amplitude):
        sineWave = utils.generateSineWave(
            frequency, amplitude, self.sampleRate, self.numSamples)
        sineWaveSampleArray = SampleArray(sampleList=sineWave)
        self._addToSamples(sineWaveSampleArray)

    def getWavBinary(self):
        wavBinary = utils.generateWavHeader(
            self.sampleRate, 2, self.numSamples)
        for sample in self.sampleArrayNormalized.getSamples():
            wavBinary += utils.normalizedSampleToWavBytes(sample)
        return wavBinary

    def _addToSamples(self, sampleArray):
        self.sampleArrayNormalized.addSampleArray(
            sampleArray, floor=-1, ceiling=1)
