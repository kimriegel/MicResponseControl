import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import pyfar as pf

from data.loader import load_file
from data.detector import detect_data_start, detect_time_column, detect_signal_column, detect_units  
#from channel import 

def main(): 
    load_file()
    
    system = choose_option ("What type of calculation method would you like to use? (Note: Automatic may not always work):", ["Automatic", "Manual"])
              
    sensitivity = int(input("Microphone Sensitivity (mV/Pa): ")).strip()
       
    offset = float(input("Voltage Offset (V): ")).strip()
    
    if system == "Automatic": 
        detect_data_start()
        detect_time_column()
        detect_signal_column()
        detect_units()

    else: 
        channel = choose_option("How many channels were used?:", ["1", "2", "3"])
        input = choose_option("What unit of input was used?:", ["Volts (V)", "Pascals (Pa)"])
        rows = int(input("How many rows need to be skipped before there's data? ")).strip()

    revised_df = pd.DataFrame({
        'Frequency': frequency,
        'Magnitude_dB': dB
    })

    revised_df.to_csv(csv_output, index=False)

    print("New files are now saved to your system.")

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

if __name__ == "__main__": 
    main()
