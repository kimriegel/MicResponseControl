#How to save png with JavaScript graphing library? 

import pandas as pd

def save_results_csv(channels, csv_output):
    if not channels:
        raise ValueError("No channels to export.")

    results = {
        "Frequency (Hz)": channels[0].frequency
    }

    for channel in channels:
        if channel.frequency is None or channel.decibels is None:
            raise ValueError(
                f"{channel.name} has no calculated frequency response."
            )

        if len(channel.frequency) != len(channel.decibels):
            raise ValueError(
                f"{channel.name} has mismatched frequency and decibel data."
            )

        results[f"{channel.name} (dB)"] = channel.decibels

    data = pd.DataFrame(results)
    data.to_csv(csv_output, index=False)
