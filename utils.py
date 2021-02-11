import numpy as np


def bytesToInt16List(binaryIn):
    return np.array([int.from_bytes(binaryIn[i:i+2], byteorder='little', signed=True) for i in range(0, len(binaryIn), 2)])
