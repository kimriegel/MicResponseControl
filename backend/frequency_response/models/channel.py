from dataclasses import dataclass
from typing import Optional

import numpy as np

@dataclass
class Channel:
    name: str
    time: np.ndarray
    raw_data: np.ndarray
    frequency: Optional[np.ndarray] = None
    decibels: Optional[np.ndarray] = None

    def __post_init__(self):
        self.time = np.asarray(self.time, dtype=float)
        self.raw_data = np.asarray(self.raw_data, dtype=float)

        self.validate_channel()

    def validate_channel(self):
        if len(self.time) != len(self.raw_data):
            raise ValueError("Time and signal data must have equal lengths.")

        if not np.all(np.isfinite(self.time)):
            raise ValueError("Time data contains invalid values.")

        if not np.all(np.isfinite(self.raw_data)):
            raise ValueError("Signal data contains invalid values.")

        if not np.all(np.diff(self.time) > 0):
            raise ValueError("Time values must be increasing.")
