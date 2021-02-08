from audioWaveForm import AudioWaveForm

audioWaveForm = AudioWaveForm(sampleRate=128000, numSamples=5 * 128000)
audioWaveForm.addSineWave(120, 0.5)
audioWaveForm.addSineWave(800, 0.2)
audioWaveForm.addSineWave(8000, 0.08)
f = open("test.wav", "w")
f.write(audioWaveForm.getWavBinary())
f.close()
