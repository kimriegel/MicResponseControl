import pandas as pd 
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

def load_file(): 
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

def create_output_names(csv_file, output_name=None):
    csv_file = Path(csv_file)

    if output_name is None:
        base_name = csv_file.stem
    else:
        base_name = Path(output_name).stem

    csv_output = csv_file.parent / f"{base_name}_revised.csv"
    png_output = csv_file.parent / f"{base_name}_revised.png"

    return csv_output, png_output

def read_data(csv_file, data_start): 
    data = pd.read_csv(csv_file, skiprows=data_start, header=None)
    data = data.dropna(axis=1, how="all")
    return data
