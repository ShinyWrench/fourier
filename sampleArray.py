class SampleArray:
    def __init__(self, numSamples=None, sampleList=None):
        if numSamples != None:
            self.samples = [0 for i in range(numSamples)]
        elif sampleList != None:
            self.samples = sampleList
        else:
            self.samples = []

    def getSamples(self):
        return [sample for sample in self.samples]

    def addSampleArray(self, sampleArray, floor=None, ceiling=None):
        samplesToAdd = sampleArray.getSamples()
        for i, ownSample in enumerate(self.samples):
            sum_ = ownSample + samplesToAdd[i]
            if ceiling != None and sum_ > ceiling:
                sum_ = ceiling
            if floor != None and sum_ < floor:
                sum_ = floor
            self.samples[i] = sum_
