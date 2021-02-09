from audioWaveForm import AudioWaveForm

AudioWaveForm = AudioWaveForm(sampleRate=128000, numSamples=5 * 128000)

# AudioWaveForm.addSineWave(120, 0.5)
# AudioWaveForm.addSineWave(800, 0.2)
# AudioWaveForm.addSineWave(8000, 0.08)

AudioWaveForm.addSineWave(440, 0.8)
AudioWaveForm.addSineWave(350, 0.8)

AudioWaveForm.writeWav()

# fourier.getConstituentFrequencies(AudioWaveForm.getSamples(), sampleRate=128000)
