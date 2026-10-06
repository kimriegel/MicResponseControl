import numpy as np
import pandas as pd
import pyfar as pf
from smoothing import smooth_frequency_response

def calculate_frequency_response(time, signal): 
    sampling_rate = 1.0 / (time[1] - time[0])
    pyfar_signal = pf.Signal(signal, sampling_rate)
    fraction = 24
    smooth_frequency_response(pyfar_signal, fraction)

