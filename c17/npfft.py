import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load time-series data
df = pd.read_csv("output_time_series.txt", header=None, names=["time", "signal", "value"])

# Filter for a specific signal
signal_name = "N19"  # Replace with your signal of interest
signal_data = df[df["signal"] == signal_name]

# Convert to numerical values (handle 'x' and 'z' appropriately)
signal_data["value"] = signal_data["value"].replace({"0": 0, "1": 1}).astype(float)

# Perform FFT
time = signal_data["time"].values
values = signal_data["value"].values
fft_result = np.fft.fft(values)

# Compute frequencies for plotting
sampling_rate = 1 / np.mean(np.diff(time))  # Assuming uniform sampling
freqs = np.fft.fftfreq(len(values), d=1/sampling_rate)

# Plot the FFT result
plt.figure(figsize=(12, 6))

# Amplitude spectrum
plt.subplot(2, 1, 1)
plt.plot(freqs[:len(freqs)//2], np.abs(fft_result)[:len(freqs)//2])  # Single-sided spectrum
plt.title("FFT Amplitude Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.grid()

# Phase spectrum
plt.subplot(2, 1, 2)
plt.plot(freqs[:len(freqs)//2], np.angle(fft_result)[:len(freqs)//2])  # Single-sided spectrum
plt.title("FFT Phase Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Phase (radians)")
plt.grid()

# Show plot
plt.tight_layout()
plt.show()

