import matplotlib.pyplot as plt

def plot_channels(channels):
    plt.figure(figsize=(10, 5), dpi=150) 
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True, which="both", ls="--")

    for channel in channels:
        plt.semilogx(channel.frequency, channel.decibels, linewidth = 1.2)
        label = channel.name

    plt.legend()

    plt.show()
