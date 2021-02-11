import matplotlib.pyplot as plt
import numpy as np
from soundBuilder import SoundBuilder
import pdb

# soundBuilder = SoundBuilder(sampleRate=44100, numSamples=3 * 44100)
soundBuilder = SoundBuilder(sampleRate=44100, numSamples=44100//10)

soundBuilder.addSineWave(120, 0.5)
soundBuilder.addSineWave(800, 0.2)
soundBuilder.addSineWave(8000, 0.08)

# soundBuilder.addSineWave(440, 0.5)
# soundBuilder.addSineWave(350, 0.5)

# soundBuilder.addSineWave(440, 1)

soundBuilder.writeWav()
soundBuilder.plotAmplitudeVsTime()
soundBuilder.plotFFT()
soundBuilder.showPlots()

# fourier.getConstituentFrequencies(SoundBuilder.getSamples(), sampleRate=128000)
