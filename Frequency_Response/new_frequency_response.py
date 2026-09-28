#Currently does not compile - needs more work done 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import pyfar as pf
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

def setup():
    root = tk.Tk()
    root.withdraw()

    downloads_path = str(Path.home() / "Downloads")

    csv_file = filedialog.askopenfilename(
            initialdir=downloads_path,
            title="Select a File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

    base_name = os.path.splitext(csv_file)[0]
    csv_output = f"{base_name}_revised.csv"
    png_output = f"{base_name}_revised.png"

    if csv_file: 
        print("File found.")
        return csv_file, base_name, csv_output, png_output
    else:
        print("No file selected.") 
        exit

def choose_option(prompt, options):
    while True:
        print(f"\n{prompt}")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")
        choice = input("Enter the number of your choice: ")

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(options):
                return options[choice - 1]
        print("Invalid choice. Please try again.")


def main(): 
    system = choose_option ("What type of calculation method would you like to use? (Note: Automatic may not always work):", ["Automatic", "Manual"])

    channel = choose_option("How many channels were used?:", ["1", "2", "3"])
      
    sensitivity = int(input("Microphone Sensitivity (mV/Pa): ")).strip()
   
    offset = float(input("Voltage Offset (V): ")).strip()

    if system == "Manual":
        input = choose_option("What unit of input was used?:", ["Volts (V)", "Pascals (Pa)"])
        rows = int(input("How many rows need to be skipped before there's data? ")).strip()
   #else: 
       # automatic()
    #print(f"Channel: {channel}")
    #print(f"Input: {input}")
    #print(f"Microphone Sensitivity: {sensitivity}")
    #print(f"Voltage Offset: {offset}")
    #print(f"Rows Skipped: {rows}")

    return channel, input, sensitivity, offset, rows


def calculate(): 
    csv_file, base_name, csv_output, png_output = setup()
    channel, input, sensitivity, offset, rows = main()

    df = pd.read_csv(csv_file, skiprows=rows, names=['Time', 'Voltage', 'Remove'])
    df = df.drop('Remove', axis=1)
    voltage = df['Voltage'].to_numpy()
    time = df['Time'].to_numpy()
    if input == "Pascals (Pa)":
        sensitivity = 40
        offset = 0.50 
        voltage = pow(10,3) * ((voltage * sensitivity) + offset)

    sampling_rate = 1.0 / (time[1] - time[0])

    #Created so pyfar library can be used 
    pyfar_signal = pf.Signal(voltage, sampling_rate)

    #1/24 Oct Smooth
    smooth_signal, _ = pf.dsp.smooth_fractional_octave(
        pyfar_signal, num_fractions=24, mode="magnitude_zerophase"
    )

    #Smoothed out versions of magnitude & freq.
    magnitude = np.abs(smooth_signal.freq.flatten())
    frequency = smooth_signal.frequencies

    N = voltage.shape[0] #Amount of samples

    magnitude = (2 / N) * magnitude
    dB = 20 * np.log10(np.maximum(magnitude, 1e-12)) #Look into comparing to 1 Pa/V

    #Graph Settings: 
    plt.figure(figsize=(10, 5), dpi=150) #figsize changes graph dimensions in inches, dpi changes resolution
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True, which="both", ls="--")

    plt.semilogx(frequency, dB, linewidth=1.2)
    plt.legend()

    #Needs to be saved before plot is shown or else it may delete graph (?)
    plt.savefig(png_output, dpi=300, bbox_inches='tight')

    plt.show()

    #Creating new .csv file 
    revised_df = pd.DataFrame({
        'Frequency': frequency,
        'Magnitude_dB': dB
    })

    revised_df.to_csv(csv_output, index=False)

    print("New files are now saved to your system.")
