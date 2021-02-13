import numpy as np
import scipy.fftpack as fftpack

# Define signal.
Fs = 128  # Sampling rate.
Ts = 1 / Fs  # Sampling interval.
Time = np.arange(0, 10, Ts)  # Time vector.
signal = np.cos(4*np.pi*Time) + np.cos(6*np.pi*Time) + np.cos(8*np.pi*Time)


def spectrum(sig, t):
    """
    Represent given signal in frequency domain.
    :param sig: signal.
    :param t: time scale.
    :return:
    """
    f = fftpack.rfftfreq(sig.size, d=t[1]-t[0])
    y = fftpack.rfft(sig)
    return f, np.abs(y)


def bandpass(f, sig, min_freq, max_freq):
    """
    Bandpass signal in a specified by min_freq and max_freq frequency range.
    :param f: frequency.
    :param sig: signal.
    :param min_freq: minimum frequency.
    :param max_freq: maximum frequency.
    :return:
    """
    return np.where(np.logical_or(f < min_freq, f > max_freq), sig, 0)


freq, spec = spectrum(signal, Time)
signal_filtered = fftpack.irfft(bandpass(freq, spec, 5, 7))

print(signal_filtered)
