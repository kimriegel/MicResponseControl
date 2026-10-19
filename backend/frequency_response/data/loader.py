#This program file is used to find and
#review a usable .csv file. 

import pandas as pd 
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

def load_file(): 
    """
    This function allows for the user to select
    a .csv file from their files folder. This is
    a quality of life improvement as opposed to having
    to name the .csv a certain name or put the file in a 
    certain location for it to work. 
    """
    root = tk.Tk()
    root.withdraw()

    downloads_path = str(Path.home() / "Downloads")

    csv_file = filedialog.askopenfilename(
            initialdir=downloads_path,
            title="Select a File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

    if csv_file:
        print("File found.")
        root.destroy()
        return csv_file
    else:
        print("No file selected.")
        root.destroy()
        return None
    # TODO : Allow for different types of file types to 
    # be used as well. Likely would make whatever other 
    # type into a .csv file before proceeding. 

def create_output_names(csv_file, output_name=None):
    """
    In order to properly name the new .csv file that will
    be produced and its png file, the names of the orignal
    are saved and then given a "_revised" at the end. This
    allows for files to be properly identified when saved to 
    the user's computer.
    """
    csv_file = Path(csv_file)

    if output_name is None:
        base_name = csv_file.stem
    else:
        base_name = Path(output_name).stem

    csv_output = csv_file.parent / f"{base_name}_revised.csv"
    png_output = csv_file.parent / f"{base_name}_revised.png"

    return csv_output, png_output
    # TODO : Consider adding a date/time to the end of file name in 
    # case a user does multiple file saves at once. 

def read_data(csv_file, data_start): 
    """
    Takes the estimated time that the data starts from 
    detect_data_start in detector.py and removes row above it. 
    It also checks if any columns are completely empty as well 
    which are also removed. This ensures no errors occur
    when analyzing the .csv file. 
    """
    data = pd.read_csv(csv_file, skiprows=data_start, header=None)
    data = data.dropna(axis=1, how="all")
    return data
