import numpy as np
import pandas as pd
import pyfar as pf
import matplotlib.pyplot as plt

def plot_channels(channels):
    plt.figure(figsize=(10, 5), dpi=150) #figsize changes graph dimensions in inches, dpi changes resolution
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True, which="both", ls="--")

    for channels in channels:
        plt.semilogx(channel.frequency, channel.dB, linewidth = 1.2)

    plt.legend()

    #plt.savefig(png_output, dpi=300, bbox_inches='tight')

    plt.show()
