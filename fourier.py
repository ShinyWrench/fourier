import matplotlib.pyplot as plt
import numpy as np
from soundBuilder import SoundBuilder
import pdb
from random import randint, random


def buildDialTone():
    soundBuilder = SoundBuilder(sampleRate=44100, numSamples=3 * 44100)
    soundBuilder.addSineWave(440, 0.5)
    soundBuilder.addSineWave(350, 0.5)
    return soundBuilder


def buildSoundWithNSineWaves(numWaves):
    soundBuilder = SoundBuilder(sampleRate=44100, numSamples=44100//2)
    for i in range(numWaves):
        frequency = randint(200, 2400)
        amplitude = random() / numWaves
        print(
            f"Add sine wave: {str(frequency).rjust(5)} Hz  {amplitude:.4f} mag.")
        soundBuilder.addSineWave(frequency, amplitude)
    return soundBuilder


def doFFTAndPlots(soundBuilder):
    soundBuilder.plotAmplitudeVsTime()
    soundBuilder.plotFFT()

    foundPeaks = soundBuilder.getFrequencyPeaksFromFFT()
    print("\nfrequency  |  magnitude")
    print("-----------------------")
    for peak in foundPeaks:
        print(
            f"{str(peak['frequency']).rjust(7)} Hz  |  {peak['magnitude']:.4f}")

    soundBuilder.showPlots()


# sbGenerated = buildSoundWithNSineWaves(10)
# sbGenerated.writeWav("generated.wav")
# doFFTAndPlots(sbGenerated)

doFFTAndPlots(
    SoundBuilder(wavFile="classical_mono.wav")
)

# fourier.getConstituentFrequencies(soundBuilder.getSamples(), sampleRate=128000)
