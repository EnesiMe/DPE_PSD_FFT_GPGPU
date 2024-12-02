import numpy as np
import matplotlib.pyplot as plt

# Example binary switching data for a signal
signal_data = [0, 1, 1, 0, 1, 0, 1, 1, 0]  # binary switching (0s and 1s)
sample_interval = 1e-9  # 1 ns sampling interval (adjust based on your VCD data)

# Convert to numpy array and apply FFT
signal_array = np.array(signal_data)
frequency_spectrum = np.fft.fft(signal_array)
frequencies = np.fft.fftfreq(len(signal_array), d=sample_interval)

# Calculate the power spectral density
power_spectral_density = np.abs(frequency_spectrum)**2

# Dynamic power estimation (simplified, scaled by an arbitrary factor)
k = 1e-15  # adjust based on capacitance, voltage, etc.
dynamic_power_estimate = k * np.sum(power_spectral_density * np.abs(frequencies))

# Plot the spectrum
plt.plot(frequencies, power_spectral_density)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density')
plt.title('Signal Power Spectrum')
plt.show()

print("Estimated Dynamic Power:", dynamic_power_estimate, "W")

