import numpy as np
import pandas as pd
import pyfar as pf


def smooth_frequency_response(pyfar_signal, fraction):
    smooth_signal, _ = pf.dsp.smooth_fractional_octave(
        pyfar_signal, num_fractions=fraction, mode="magnitude_zerophase"
    )

    magnitude = np.abs(smooth_signal.freq.flatten())
    frequency = smooth_signal.frequencies
    
    N = magnitude.shape[0] #Amount of samples

    magnitude = (2 / N) * magnitude
    dB = 20 * np.log10(np.maximum(magnitude, 1e-12)) #Look into comparing to 1 Pa/V
    return frequency, dB 
