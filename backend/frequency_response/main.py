import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyfar as pf

from data.loader import load_file, create_output_names, read_data
from data.detector import detect_data_start, detect_time_column, detect_signal_columns
from data.exporter import save_results_csv

from models.channel import Channel

from processing.frequency_response import calculate_frequency_response

from plotting.plot import plot_channels

def main(): 
    csv_file = load_file()
    csv_output, png_output = create_output_names(csv_file)

    data_start = detect_data_start(csv_file)

    data = read_data(csv_file, data_start)

    time_column = detect_time_column(data)
    signal_column = detect_signal_columns(data, time_column)

    channels = []

    for channel_number, column in enumerate(signal_column, start=1):
        channel = Channel(
            name=f"Channel {channel_number}",
            time=data[time_column].to_numpy(),
            raw_data=data[column].to_numpy()
        )
        channels.append(channel)
    for channel in channels:
        channel.frequency, channel.decibels = calculate_frequency_response(channel)

    plot_channels(channels)

    save_results_csv(channels, csv_output)

if __name__ == "__main__": 
    main()
