#Program file includes main code used to
#transition from time to frequency domain. 

import numpy as np
import pyfar as pf


def calculate_frequency_response(channel, num_fractions=24):
    """
    Uses primarily the pyfar library to calculate frequency 
    and decibels alongside their fractional smoothing. 
    """
    
    time = channel.time
    voltage = channel.raw_data

    sampling_rate = 1.0 / (time[1] - time[0])
    #Used to identify the maximum range of frequency. 

    pyfar_signal = pf.Signal(voltage, sampling_rate)
    #Converts into frequency domain with both signal values
    #and frequency values. 
    
    smooth_signal, _ = pf.dsp.smooth_fractional_octave(
        #Smooths signal depending on the fractional smooth selected.
        pyfar_signal,
        num_fractions=num_fractions,
        mode="magnitude_zerophase"
    )

    magnitude = np.abs(smooth_signal.freq.flatten())
    frequency = smooth_signal.frequencies

    N = voltage.shape[0]
    magnitude = (2 / N) * magnitude

    decibels = 20 * np.log10(np.maximum(magnitude, 1e-12))

    return frequency, decibels

