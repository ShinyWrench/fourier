import matplotlib.pyplot as plt
import numpy as np
from soundBuilder import SoundBuilder
from random import randint, random


def buildDialTone():
    SAMPLE_RATE = 8000
    # soundBuilder = SoundBuilder(sampleRate=44100, numSamples=3 * 44100)
    soundBuilder = SoundBuilder(
        sampleRate=SAMPLE_RATE, numSamples=5*SAMPLE_RATE)
    soundBuilder.addSineWave(440, 0.5)
    soundBuilder.addSineWave(350, 0.5)
    return soundBuilder


def buildSoundWithNSineWaves(numWaves):
    SAMPLE_RATE = 44100
    soundBuilder = SoundBuilder(
        sampleRate=SAMPLE_RATE, numSamples=3*SAMPLE_RATE)
    for i in range(numWaves):
        frequency = randint(200, 2400)
        amplitude = random() / numWaves
        print(
            f"Add sine wave: {str(frequency).rjust(5)} Hz  {amplitude:.4f} mag.")
        soundBuilder.addSineWave(frequency, amplitude)
    return soundBuilder


def buildToneForSpikeDiffusionTest():
    soundBuilder = SoundBuilder(
        sampleRate=300, numSamples=3300)
    soundBuilder.addSineWave(55, 1)
    soundBuilder.addSineWave(80, 0.5)
    return soundBuilder


def doFFTAndAllPlots(soundBuilder, show=True, titlePrefix=""):
    # soundBuilder.plotAmplitudeVsTime(titlePrefix)
    soundBuilder.plotAllFFTProducts()

    foundPeaks = soundBuilder.getFrequencyPeaksFromFFT()
    print("\n    Freq.   |  Ampl.  ")
    print(" -----------------------")
    for peak in foundPeaks:
        print(
            f"{('%.1f' % peak['frequency']).rjust(7)} Hz  |  {peak['magnitude']:.4f}")

    if show == True:
        soundBuilder.showPlots()


def plotBestFFTProducts(soundBuilder, show=True):
    soundBuilder.plotBestFFTProducts()

    foundPeaks = soundBuilder.getFrequencyPeaksFromFFT()
    print("\n    Freq.   |  Ampl.  ")
    print(" -----------------------")
    for peak in foundPeaks:
        print(
            f"{('%.1f' % peak['frequency']).rjust(7)} Hz  |  {peak['magnitude']:.4f}")

    if show == True:
        soundBuilder.showPlots()

# doFFTAndAllPlots(buildDialTone())

# doFFTAndAllPlots(buildSoundWithNSineWaves(10))


# plotBestFFTProducts(buildDialTone())

plotBestFFTProducts(buildSoundWithNSineWaves(10))

# doFFTAndAllPlots(
#     SoundBuilder(wavFile="classical_mono.wav")
# )

# sb = SoundBuilder(rawFile="21-02-11_17-17-02.raw", sampleRate=8000)
# WINDOW_SIZE_SECONDS = 0.1
# t_seconds = 56.5
# while t_seconds < 57.8:
#     doFFTAndAllPlots(
#         sb.getClip(startTime=t_seconds,
#                    endTime=t_seconds + WINDOW_SIZE_SECONDS),
#         show=False,
#         titlePrefix=f"{t_seconds:.2f} sec. to {t_seconds + WINDOW_SIZE_SECONDS:.2f} sec."
#     )
#     t_seconds += WINDOW_SIZE_SECONDS
# sb.showPlots()

# fourier.getConstituentFrequencies(soundBuilder.getSamples(), sampleRate=128000)
