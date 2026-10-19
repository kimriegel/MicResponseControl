#In order to allow the program to handle an
#unforeseeable amount of channels a dataclass is 
#created. 

from dataclasses import dataclass
from typing import Optional

import numpy as np

@dataclass
class Channel:
    """
    The Channel dataclass includes the name, initial values, 
    then calculated values. It allows for data surrounding 
    channels to be easily stored and scaled. 
    """
    name: str
    time: np.ndarray
    raw_data: np.ndarray
    frequency: Optional[np.ndarray] = None
    decibels: Optional[np.ndarray] = None
    #The frequency and decibels are initially considered
    #optional so that way the program will not get an error due to
    #missing values. 

    def __post_init__(self):
        """
        Gets initial signal values and time values and 
        populates the channel. 
        """
        self.time = np.asarray(self.time, dtype=float)
        self.raw_data = np.asarray(self.raw_data, dtype=float)

        self.validate_channel()

    def validate_channel(self):
        """
        Checks for noticable errors that could make the channel disfunctional,
        more so a worry with edited .csv files or with unknown formatting from DAQ
        systems. 
        """
        if len(self.time) != len(self.raw_data):
            raise ValueError("Time and signal data must have equal lengths.")

        if not np.all(np.isfinite(self.time)):
            raise ValueError("Time data contains invalid values.")

        if not np.all(np.isfinite(self.raw_data)):
            raise ValueError("Signal data contains invalid values.")

        if not np.all(np.diff(self.time) > 0):
            raise ValueError("Time values must be increasing.")
