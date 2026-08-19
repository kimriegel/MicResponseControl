import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import glob
import os
from scipy.fft import fft, fftfreq
print("Everything works")
print("NumPy:", np.__version__)
print("pandas:", pd.__version__)
print("SciPy:", scipy.__version__)

csv_files = glob.glob('*.csv')

if csv_files:
    # Get the most recently modified CSV file
    latest_file = max(csv_files, key=os.path.getmtime)
    print(f"Loading files: {latest_file}")
    
    # Import the file using pandas
    df = pd.read_csv(latest_file, skiprows = 9, names=['Time', 'Voltage', 'Remove'])#different solution may be needed if it varies
    df = df.drop('Remove', axis=1) #For some reason the sample .csv came with an additional unused column
    print(df.head())
else:
    print("No CSV files found in the directory.")

voltage = df['Voltage'].to_numpy()
time = df['Time'].to_numpy()

voltage = voltage - np.mean(voltage) #may be removing DC offset if it exists

X = fft(voltage)
print(X)
magnitude = np.abs(X)

N = voltage.shape[0]

dt = time[1] - time[0]
frequency = fftfreq(N, d=dt)

frequency = frequency[:N//2]
magnitude = magnitude[:N//2]
magnitude = (2/N) * magnitude 
dB = 20 * np.log10(np.maximum(magnitude, 1e-12))

print("Positive Only")
print("Frequency:")
print(frequency)

print("Magnitude:")
print(magnitude)

plt.semilogx(magnitude, dB)
plt.show()
