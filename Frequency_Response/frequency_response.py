import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import pyfar as pf

csv_files = "test.csv"

if csv_files:
    print(f"Loading file: {csv_files}")
else:
    print("No CSV files found in the directory.")
    exit()

base_name = os.path.splitext(csv_files)[0]
csv_output = f"{base_name}_revised.csv"
png_output = f"{base_name}_revised.png"

def singular(): 
    df = pd.read_csv(csv_files, skiprows=9, names=['Time', 'Voltage', 'Remove'])
    df = df.drop('Remove', axis=1)
    voltage = df['Voltage'].to_numpy()
    time = df['Time'].to_numpy()
    if pascal == True:
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
    #Pre-set domain and range needs to be edited to calculate the fit
    #plt.xlim(20, sampling_rate / 2) 
    #plt.ylim(-120, -60)
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
    
def double():
    #df = pd.read_csv(latest_file, skiprows=9, names=['Time', 'Voltage1', 'Voltage2', 'Remove'])
    df = pd.read_csv(csv_files, skiprows=9, names=['Time', 'Voltage1', 'Voltage2', 'Remove'])
    df = df.drop('Remove', axis=1)
    #Extracted from .csv 
    time = df['Time'].to_numpy()
    voltage1 = df['Voltage1'].to_numpy()
    voltage2 = df['Voltage2'].to_numpy()
    if pascal == True:
        sensitivity = 40
        offset = 0.50 
        voltage1 = pow(10,3) * ((voltage1 * sensitivity) + offset)

    if pascal == True:
        sensitivity = 40
        offset = 0.50 
        voltage2 = pow(10,3) * ((voltage2 * sensitivity) + offset)
    
    sampling_rate = 1.0 / (time[1] - time[0])

    pyfar_signal1 = pf.Signal(voltage1, sampling_rate)

    smooth_signal1, _ = pf.dsp.smooth_fractional_octave(
        pyfar_signal1,
        num_fractions=24,
        mode="magnitude_zerophase"
    )

    magnitude1 = np.abs(smooth_signal1.freq.flatten())
    frequency1 = smooth_signal1.frequencies
    
    N1 = voltage1.shape[0] #Amount of samples
    
    magnitude1 = (2 / N1) * magnitude1
    dB1 = 20 * np.log10(np.maximum(magnitude1, 1e-12)) #Look into comparing to 1 Pa/V

    pyfar_signal2 = pf.Signal(voltage2, sampling_rate)
    
    smooth_signal2, _ = pf.dsp.smooth_fractional_octave(
            pyfar_signal2,
            num_fractions=24,
            mode="magnitude_zerophase"
    )
    
    magnitude2 = np.abs(smooth_signal2.freq.flatten())
    frequency2 = smooth_signal2.frequencies
        
    N2 = voltage2.shape[0] #Amount of samples
        
    magnitude2 = (2 / N2) * magnitude2
    dB2 = 20 * np.log10(np.maximum(magnitude2, 1e-12)) #Look into comparing to 1 Pa/V

    plt.figure(figsize=(10, 5), dpi=150)

    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True, which="both", ls="--")

    plt.semilogx(
        frequency1,
        dB1,
        linewidth=1.2,
        label='Channel 1'
    )

    plt.semilogx(
        frequency2,
        dB2,
        linewidth=1.2,
        label='Channel 2'
    )

    plt.legend()

    #Needs to be saved before plot is shown or else it may delete graph (?)
    plt.savefig(png_output, dpi=300, bbox_inches='tight')

    plt.show()

    revised_df = pd.DataFrame({
        'Frequency': frequency1,
        'Magnitude_dB_1': dB1,
        'Magnitude_dB_2': dB2
    })

    revised_df.to_csv(csv_output, index=False)

    print("New files are now saved to your system.")

while ((answer != 1) and (answer != 2)):
    #answer = int(input("Are you measuring in volts or pascals? (TYPE: '1' - volts or '2' - pascals)"))
    #if (answer == 2):
        #pascal = True
    answer = int(input("How many channels were measured? (TYPE: '1'  or  '2')"))
    break 
 
if (answer == 1):
    singular()
if (answer == 2):
    double()
