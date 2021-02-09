import math


def generateSineWave(frequency, amplitude, sampleRate, numSamples):
    # TODO: Verify this works by eye in Audacity
    radiansPerSample = 2 * math.pi * frequency / sampleRate
    return [amplitude * math.sin(i * radiansPerSample) for i in range(numSamples)]
