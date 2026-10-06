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
        return #csv_file, base_name, csv_output, png_output
    else:
        print("No file selected.") 
        exit

