import math


def generateSineWave(frequency, amplitude, sampleRate, numSamples):
    samples = []
    radiansPerSample = 2 * math.pi * frequency / sampleRate
    for i in range(numSamples):
        samples.append(amplitude * math.sin(i * radiansPerSample))
    return samples


def normalizedSampleToWavBytes(normalizedSample):
    unsigned16BitInteger = int((normalizedSample + 1) * 0x8000)
    if unsigned16BitInteger > 0xFFFF:
        unsigned16BitInteger = 0xFFFF
    signed16BitInteger = unsigned16BitInteger - 0x8000
    LSB = signed16BitInteger & 0xFF
    MSB = (signed16BitInteger >> 8) & 0xFF
    return chr(LSB) + chr(MSB)


def generateWavHeader(sample_rate, bytes_per_sample, data_length):

    def headerValueToBytes(value, size, endian="big"):

        if endian == "big":
            shift_list = range(size - 1, -1, -1)
        else:
            shift_list = range(size)
        output = ""
        for index in shift_list:
            output += chr((value >> (index * 8)) & 0xFF)
        return output

    # 0-3  ChunkID: "RIFF" (b-e)
    header = headerValueToBytes(0x52494646, 4)
    # 4-7  ChunkSize: 36 + subchunk2 size (l-e)
    header += headerValueToBytes(36 + data_length, 4, endian="little")
    # 8-11  Format: "WAVE" (b-e)
    header += headerValueToBytes(0x57415645, 4)
    # 12-15  Subchunk1ID: "fmt " (b-e)
    header += headerValueToBytes(0x666d7420, 4)
    # 16-19  Subchunk1Size: 16 (l-e)
    header += headerValueToBytes(16, 4, endian="little")
    # 20-21  AudioFormat: 1 (l-e)
    header += headerValueToBytes(1, 2, endian="little")
    # 22-23  NumChannels: 1 (l-e)
    header += headerValueToBytes(1, 2, endian="little")
    # 24-27  SampleRate:  specified above (l-e)
    header += headerValueToBytes(sample_rate, 4, endian="little")
    # 28-31  ByteRate:  bytes per second (l-e)
    header += headerValueToBytes(sample_rate *
                                 bytes_per_sample, 4, endian="little")
    # 32-33  BlockAlign:  bytes per sample (l-e)
    header += headerValueToBytes(bytes_per_sample, 2, endian="little")
    # 34-35  BitsPerSample: bits per sample (l-e)
    header += headerValueToBytes(16, 2, endian="little")
    # 36-39  Subchunk2ID: "data" (b-e)
    header += headerValueToBytes(0x64617461, 4)
    # 40-43  Subchunk2Size: number of bytes in data (l-e)
    header += headerValueToBytes(data_length, 4, endian="little")

    return header
