from gui.modulation.Modulation import ModulationFactory
import numpy as np
from scipy import signal as sig
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from gui.networking.xi import XIPacket

# msg = 'hello'
msg = [chr(ord('a') + (x % 26)) for x in range(2**10 - 1)]
m = 4**2
# scheme = ModulationFactory.chooseScheme('qpsk')
scheme = ModulationFactory.chooseScheme('qam', m=m)
start = timer()
symbols = scheme.symbolMap(msg)
print("%d-QAM Symbol Map time: %fms" % (m, (timer() - start) * 1e3))

start = timer()
out = scheme.symbolDemap(symbols)
print("%d-QAM Symbol demap time: %fms" % (m, (timer() - start) * 1e3))
start = timer()
out = scheme.symbolVectorizedDemap(symbols)
print("%d-QAM Symbol Vectorized demap time: %fms" % (m,
                                                     (timer() - start) * 1e3))
out = "".join([chr(x) for x in out])
print(out)

scheme.D = 2
scheme.P = 3
scheme.alpha = 0.3

print("D: %d, P: %d, alpha: %f" % (scheme.D, scheme.P, scheme.alpha))

msg = [chr(ord('a') + (x % 26)) for x in range(2**10 - 1)]
# msg = "hello world"
# msg = "abcd efgh ijkl mnop qrst uvwxyz 1234567890 $$*$$"
start = timer()
packet = XIPacket(buffer=msg)
s = scheme.modulateData(packet.rep)
end = timer()
print("Mod time: %fms" % ((end - start) * 1e3))

# Simulated Channel
t0 = 0  # channel delay
A = 2**11  # channel gain
h = A * np.append(np.zeros(t0, dtype=int), [1])

r = sig.convolve(s, h)
r = 0.6 * r + 0.4 * np.random.randn(len(r))  # add in noise
r = np.concatenate((r, r, r))

start = timer()
unfiltered = scheme.unfilterData(r)
print("Unfilter data: %fms" % ((timer() - start) * 1e3))

start = timer()
buffer = scheme.demodulateData(r, showAllPlots=True)
packet = XIPacket.createXIPacket(buffer=buffer)
strOut = packet.payload if packet is not None else ""
end = timer()
print("Total demod time: %fms" % ((end - start) * 1e3))
print(strOut)