#Technically the plot created by matplotlib is not
#used within the frontend because the library always
#creates a new window for its plot. However, the 
#logic used here is still reused and can also be 
#important for backend testing. 

import matplotlib.pyplot as plt

def plot_channels(channels):
    """
    Used to graph an unforeseeable amount of channels
    at once. Sets up basic settings of the graph and 
    then iteratively adds each channel to the graph 
    as well. 
    """
    plt.figure(figsize=(10, 5), dpi=150) 
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True, which="both", ls="--")

    for channel in channels:
        plt.semilogx(channel.frequency, channel.decibels, linewidth = 1.2)
        label = channel.name

    plt.legend()

    plt.show()
