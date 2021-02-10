from soundBuilder import SoundBuilder

SoundBuilder = SoundBuilder(sampleRate=128000, numSamples=5 * 128000)

# SoundBuilder.addSineWave(120, 0.5)
# SoundBuilder.addSineWave(800, 0.2)
# SoundBuilder.addSineWave(8000, 0.08)

SoundBuilder.addSineWave(440, 0.8)
SoundBuilder.addSineWave(350, 0.8)

SoundBuilder.writeWav()

# fourier.getConstituentFrequencies(SoundBuilder.getSamples(), sampleRate=128000)
