import numpy as np
import pyfar as pf


def calculate_frequency_response(channel, num_fractions=24):
    time = channel.time
    voltage = channel.raw_data

    sampling_rate = 1.0 / (time[1] - time[0])

    pyfar_signal = pf.Signal(voltage, sampling_rate)

    smooth_signal, _ = pf.dsp.smooth_fractional_octave(
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

