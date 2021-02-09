import numpy as np
import utils
import wave
import struct


class AudioWaveForm:

    def __init__(self, sampleRate, numSamples):
        self.sampleRate = sampleRate
        self.numSamples = numSamples
        self.samples_float = np.zeros(self.numSamples)

    def addSineWave(self, frequency, amplitude):
        sineWave = utils.generateSineWave(
            frequency, amplitude, self.sampleRate, self.numSamples)
        self.samples_float = np.add(self.samples_float, sineWave)

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
