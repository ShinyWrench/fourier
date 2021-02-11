import matplotlib.pyplot as plt
import numpy as np
from soundBuilder import SoundBuilder
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

# doFFTAndPlots(
#     SoundBuilder(wavFile="classical_mono.wav")
# )

sb = SoundBuilder(rawFile="21-02-11_17-17-02.raw", sampleRate=8000)
sb.writeWav("didItWork.wav")

# sb = SoundBuilder(rawFile="21-02-11_17-17-02.raw", sampleRate=8000)
# WINDOW_SIZE_SECONDS = 0.1
# for t_seconds in range(54.2, 54.7, WINDOW_SIZE_SECONDS):
#     doFFTAndPlots(sb.getClip(startTime=t_seconds,
#                              endTime=t_seconds + WINDOW_SIZE_SECONDS))

# fourier.getConstituentFrequencies(soundBuilder.getSamples(), sampleRate=128000)
