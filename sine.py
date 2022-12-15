
import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt


# Set the parameters for the sine wave
frequency = 440  # Hz
duration = 2.0   # seconds
amplitude = 0.5  # amplitude of the sine wave

# Generate the time points for the sine wave
t = np.linspace(0, duration, int(duration * 44100))

# Generate the sine wave
y = amplitude * np.sin(2 * np.pi * frequency * t)
print(y)
# Create a figure and axes
fig, ax = plt.subplots()

# Plot the data
ax.plot(t, y)

# Convert the signal to 16-bit integer values
y = y * 32767
y = y.astype(np.int16)

# Write the signal to a WAV file
write("sine.wav", 44100, y)
