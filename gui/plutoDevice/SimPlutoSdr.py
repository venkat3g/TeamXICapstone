import numpy as np
from scipy import signal as sig

class _SimCtx():
    def __init__(self):
        self.name = "Sim"

class SimPlutoSdr():
    def __init__(self):
        self.ctx = _SimCtx()

        # RX Information
        self.sampling_frequency = 3.0
        self.rx_lo_freq = 2400.0
        self.rx_bandwidth = 20.0
        self.rx_decimation = 0.0
        self.rx_gain = 10.0

        # TX Information
        self.tx_lo_freq = 2400.0
        self.tx_bandwidth = 20.0
        self.tx_interpolation = 0.0
        self.tx_gain = -10.0

        # Simulate Buffer
        self._buffer = None

    def writeTx(self, data, raw=False):
        # Simulated Channel
        t0 = 0 # channel delay
        A = 2**12 # channel gain
        h = A * np.append(np.zeros(t0, dtype=int), [1])

        r = sig.convolve(data, h)
        r = r + 0.4 * np.random.randn(len(r)) # add in noise
        self._buffer = r

    def readRx(self, num_samples, raw=False):
        a = np.zeros(num_samples, complex)
        a[0:len(self._buffer)] = self._buffer
        return a