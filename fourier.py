from audioSegment import AudioSegment

AudioSegment = AudioSegment(sampleRate=128000, numSamples=5 * 128000)

# AudioSegment.addSineWave(120, 0.5)
# AudioSegment.addSineWave(800, 0.2)
# AudioSegment.addSineWave(8000, 0.08)

AudioSegment.addSineWave(440, 0.8)
AudioSegment.addSineWave(350, 0.8)

AudioSegment.writeWav()

# fourier.getConstituentFrequencies(AudioSegment.getSamples(), sampleRate=128000)
