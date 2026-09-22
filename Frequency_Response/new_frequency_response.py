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

def main(): 
   csv_file, base_name, csv_output, png_output = setup()

   print(csv_file)
   print(base_name)
   print(csv_output)
   print(png_output)



main()

