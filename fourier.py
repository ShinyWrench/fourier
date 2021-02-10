import matplotlib.pyplot as plt
import numpy as np
from soundBuilder import SoundBuilder
import pdb

# soundBuilder = SoundBuilder(sampleRate=44100, numSamples=3 * 44100)
soundBuilder = SoundBuilder(sampleRate=100, numSamples=100)

# soundBuilder.addSineWave(120, 0.5)
# soundBuilder.addSineWave(800, 0.2)
# soundBuilder.addSineWave(8000, 0.08)

# soundBuilder.addSineWave(440, 0.5)
# soundBuilder.addSineWave(350, 0.5)

soundBuilder.addSineWave(3, 1)

soundBuilder.writeWav()
# soundBuilder.plotAmplitudeVsTime()

fftResult = np.fft.fft(soundBuilder.getSamples())

plt.figure()
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
# plt.plot(range(len(fftResult)), np.abs([n for n in fftResult]))
plt.plot(
    np.linspace(0, 100/2, int(len(fftResult)/2)),
    np.abs(fftResult[:int(len(fftResult)/2)])
)
plt.show()

# pdb.set_trace()
# plt.plot(
#     np.linspace(0, 44100 / 2, 3* 44100 / 2),

# )


# fourier.getConstituentFrequencies(SoundBuilder.getSamples(), sampleRate=128000)
