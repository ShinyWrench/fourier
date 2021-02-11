import matplotlib.pyplot as plt
import numpy as np
from soundBuilder import SoundBuilder
import pdb
from random import randint, random

# soundBuilder = SoundBuilder(sampleRate=44100, numSamples=3 * 44100)
soundBuilder = SoundBuilder(sampleRate=44100, numSamples=44100//2)


# soundBuilder.addSineWave(120, 0.5)
# soundBuilder.addSineWave(800, 0.2)
# soundBuilder.addSineWave(8000, 0.08)

# soundBuilder.addSineWave(440, 0.5)
# soundBuilder.addSineWave(350, 0.5)

# soundBuilder.addSineWave(440, 1)

NUM_WAVES = 10
for i in range(NUM_WAVES):
    frequency = randint(200, 2400)
    amplitude = random() / NUM_WAVES
    print(f"Add sine wave: {str(frequency).rjust(5)} Hz  {amplitude:.4f} mag.")
    soundBuilder.addSineWave(frequency, amplitude)

soundBuilder.writeWav()
soundBuilder.plotAmplitudeVsTime()
soundBuilder.plotFFT()

foundPeaks = soundBuilder.getFrequencyPeaksFromFFT()
print("\nfrequency  |  magnitude")
print("-----------------------")
for peak in foundPeaks:
    print(
        f"{str(peak['frequency']).rjust(7)} Hz  |  {peak['magnitude']:.4f}")

soundBuilder.showPlots()

# fourier.getConstituentFrequencies(SoundBuilder.getSamples(), sampleRate=128000)
