import numpy as np
import matplotlib.pyplot as plt
import pycuda.autoinit
import pycuda.gpuarray as gpuarray
from skcuda.fft import Plan, fft

# Provided VCD time series data
data = [
    [0, "N22", 0],
    [0, "N19", 1],
    [0, "N16", 1],
    [0, "N11", 1],
    [0, "N10", 1],
    [0, "N7", 0],
    [0, "N6", 0],
    [0, "N3", 0],
    [0, "N2", 0],
    [0, "N1", 0],
    [0, "N23", 0],
    [10000, "N6", 1],
    [10000, "N1", 1],
    [20000, "N22", 1],
    [20000, "N23", 1],
    [20000, "N19", 0],
    [20000, "N16", 0],
    [20000, "N7", 1],
    [20000, "N2", 1],
    [30000, "N6", 0],
    [30000, "N3", 1],
    [30000, "N1", 0],
    [40000, "N23", 0],
    [40000, "N16", 1],
    [40000, "N19", 1],
    [40000, "N11", 0],
    [40000, "N10", 0],
    [40000, "N6", 1],
    [40000, "N1", 1]
]

# Convert the data into a structured NumPy array
signals = ["N22", "N19", "N16", "N11", "N10", "N7", "N6", "N3", "N2", "N1", "N23"]
time_steps = sorted(set(row[0] for row in data))
time_series = {signal: np.zeros(len(time_steps)) for signal in signals}

# Fill time-series data
time_to_index = {time: i for i, time in enumerate(time_steps)}
for time, signal, value in data:
    time_series[signal][time_to_index[time]] = value

# Define cuFFT parameters and perform FFT for each signal
def perform_fft_with_cufft(signal_data, time_steps):
    sample_interval = (time_steps[1] - time_steps[0]) * 1e-9  # Convert ns to seconds
    num_samples = len(signal_data)

    # Transfer data to GPU
    signal_gpu = gpuarray.to_gpu(signal_data.astype(np.complex64))

    # Create FFT plan
    fft_plan = Plan(num_samples, np.complex64, np.complex64)

    # Perform FFT on GPU
    fft_result_gpu = gpuarray.empty_like(signal_gpu)
    fft(signal_gpu, fft_result_gpu, fft_plan)

    # Transfer FFT result back to CPU
    fft_result = fft_result_gpu.get()

    # Calculate frequencies and power spectral density
    frequencies = np.fft.fftfreq(num_samples, d=sample_interval)
    power_spectral_density = np.abs(fft_result) ** 2

    return frequencies, power_spectral_density

# Perform FFT for each signal and calculate dynamic power estimation
V_dd = 1.8  # Voltage in volts
C_L = 10e-15  # Load capacitance in farads
f = 1e9  # Frequency in Hz (1 GHz)
total_dynamic_power = 0

for signal, signal_data in time_series.items():
    frequencies, power_spectral_density = perform_fft_with_cufft(signal_data, time_steps)
    
    # Estimate switching activity (alpha) from power spectral density
    alpha = np.sum(power_spectral_density) / len(signal_data)

    # Calculate dynamic power for this signal
    power = alpha * C_L * (V_dd ** 2) * f
    total_dynamic_power += power

    # Visualize FFT (optional)
    plt.plot(frequencies[:len(frequencies)//2], power_spectral_density[:len(frequencies)//2], label=f"{signal}")

# Plot results
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density')
plt.title('FFT Analysis of Signals')
plt.legend(loc='upper right')
plt.grid()
plt.show()

# Output total dynamic power
total_dynamic_power

