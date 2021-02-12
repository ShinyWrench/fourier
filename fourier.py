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
    soundBuilder = SoundBuilder(sampleRate=44100, numSamples=44100*2)
    for i in range(numWaves):
        frequency = randint(200, 2400)
        amplitude = random() / numWaves
        print(
            f"Add sine wave: {str(frequency).rjust(5)} Hz  {amplitude:.4f} mag.")
        soundBuilder.addSineWave(frequency, amplitude)
    return soundBuilder


def doFFTAndPlots(soundBuilder, show=True, titlePrefix=""):
    # soundBuilder.plotAmplitudeVsTime(titlePrefix)
    # soundBuilder.plotFFT(titlePrefix)
    soundBuilder.plotAllFFTProducts()

    foundPeaks = soundBuilder.getFrequencyPeaksFromFFT()
    print("\nfrequency  |  magnitude")
    print("-----------------------")
    for peak in foundPeaks:
        print(
            f"{str(peak['frequency']).rjust(7)} Hz  |  {peak['magnitude']:.4f}")

    if show == True:
        soundBuilder.showPlots()


# doFFTAndPlots(buildDialTone())

sbGenerated = buildSoundWithNSineWaves(10)
sbGenerated.writeWav("generated.wav")
doFFTAndPlots(sbGenerated)

# doFFTAndPlots(
#     SoundBuilder(wavFile="classical_mono.wav")
# )

# sb = SoundBuilder(rawFile="21-02-11_17-17-02.raw", sampleRate=8000)
# WINDOW_SIZE_SECONDS = 0.1
# t_seconds = 56.5
# while t_seconds < 57.8:
#     doFFTAndPlots(
#         sb.getClip(startTime=t_seconds,
#                    endTime=t_seconds + WINDOW_SIZE_SECONDS),
#         show=False,
#         titlePrefix=f"{t_seconds:.2f} sec. to {t_seconds + WINDOW_SIZE_SECONDS:.2f} sec."
#     )
#     t_seconds += WINDOW_SIZE_SECONDS
# sb.showPlots()

# fourier.getConstituentFrequencies(soundBuilder.getSamples(), sampleRate=128000)
