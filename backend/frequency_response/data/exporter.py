#Used when user presses the save button for the new .csv file. 
#This new file contains frequency in place of time, and dB in
#place of the initial signal. 

import pandas as pd

def save_results_csv(channels, csv_output):
    """
    To make the process of analyzing frequency response
    easier, the user can download the new .csv file
    with calculated frequency and dB values that can then
    be put into a spreadsheet program such as Excel or 
    Google Sheets. The program does basic error detection
    before saving to ensure a corrupted file is not produced. 
    """
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
