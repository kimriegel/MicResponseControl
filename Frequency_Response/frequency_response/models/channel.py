from dataclasses import dataclass

@dataclass
class Channel:
    name: str
    raw_data: float
    time: float
    unit: str
    sensitivity: float
    voltage_offset: float 

    converted_data: float

    frequency: float
    magnitude: float
    decibels: float
    smoothed_frequency:float
    smoothed_decibels:float

def initialize_channel():

