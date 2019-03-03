from filter import srrc
from Modulation import ModulationFactory
import numpy as np
import matplotlib.pyplot as plt
import random


fc = 12000
fs = 44100

Ts = 1.0 / fs

# Pulse Shaping Filter
P = 110
D = 4
alpha = 0.1
g = srrc(D, alpha, P)

# Pilot Sequence - Barker code
pilots = [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]

# message to be sent - string
i = "hello world!"

# upsampling pilots
a = list(pilots)
aup = np.zeros(len(pilots)*P, dtype=float)
_index_a = 0
for x in range(0, len(aup), P):
    aup[x] = a[_index_a]
    _index_a += 1

# symbol mapping
scheme = ModulationFactory.chooseScheme('qam')
symbols = scheme.symbolMap(i, False)

# create packet by concatenating pilots with data
packet = list(pilots)
packet.extend(symbols)

# upsample packet
packetup = np.zeros(len(packet)*P, dtype=complex)
_index_packet = 0
for x in range(0, len(packetup), P):
    packetup[x] = packet[_index_packet]
    _index_packet += 1

# convolve packetup with pulse shaping filter g
m = np.convolve(packetup, g)

# plt.plot(np.arange(0, Ts, Ts/len(m)), m)

# modulate message
t_s = np.arange(0, len(m) * Ts, Ts)
s = np.array([(m[i] * np.exp(1.j * 2 * np.pi * fc * t_s[i])).real for i in range(len(m))])

# Simulated Channel
t0 = 9 # channel delay
A = 7 # channel gain
h = A * np.append(np.zeros(t0, dtype=int), [1])

r = np.convolve(s, h)
r = r + 0.4 * np.random.randn(len(r)) # add in noise

# Rx side
fOff = 7 # frequency offset of oscillator
phiOff = 0.4 # phase offset of oscillator

# demodulate w/ freq and phase offset
t_v = np.arange(0, len(r) * Ts, Ts)
v = 2*r*np.exp(-1.j*(2*np.pi*(fc+fOff)*t_v+phiOff))

# convolve demodulated signal with pulse shaping filter
yup = np.convolve(v, g)

# time framing sync using correlation
timingTest = np.convolve(yup, np.flip(aup))
absTimingTest = np.abs(timingTest)
peakMag = absTimingTest.max()
peakIndex = np.argmax(absTimingTest)

# index of first pilot symbol
t0 = peakIndex - len(aup) + 1;

# get pilots and data from upsampled y
y = yup[t0:t0+len(packetup)-1: P]
yPilots = y[0:len(pilots)]
yData = y[len(pilots):]
# plt.scatter(yData.real, yData.imag)

# freq and phase error correction
phaseError = np.unwrap(np.angle(yPilots / a))
lineFit = np.polyfit(range(len(pilots)), phaseError, 1)
slope = lineFit[0]
intercept = lineFit[1]
line = slope*np.arange(len(pilots))+intercept

# phase error plot
# plt.plot(range(len(pilots)), line) 
# plt.scatter(range(len(pilots)), phaseError)

# Freq and Phase Offsets
T = P / fs
f0 = -slope / (2 * np.pi * T) # T or Ts?
phi = -1 * intercept
phideg = phi * 180.0 / np.pi

# Correct for freq and phase offset
n = np.arange(len(pilots), len(packet))
syncData = yData * np.exp(-1.j * (slope * n + intercept))

# final constellation
plt.scatter(syncData.real, syncData.imag)

# undo symbol mapping
strOut = scheme.symbolDemap(syncData, False)
print("".join([chr(c) for c in strOut]))

plt.show()