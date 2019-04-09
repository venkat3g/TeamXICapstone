import numpy as np
from scipy import signal as sig
from timeit import default_timer as timer
import time


class _SimCtx():
    def __init__(self):
        self.name = "Sim"


FLOAT = np.float64
COMPLEX = np.complex128


class SimPlutoSdr():
    def __init__(self, P, alpha, desiredBandwidth):
        self.ctx = _SimCtx()

        # RX Information
        self.sampling_frequency = P * desiredBandwidth / (1 + alpha)
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
        self._buffer = np.zeros(2**18)
        # Timer used to simulate sampling frequency
        self._lastRead = 0
        self.no_bits = 12

    def raw2complex(self, data):
        """return a scaled complex float version of the raw data"""
        # convert to float64, view performs an in place recast of the data
        # from SO 5658047
        # are the #bits available from some debug attr?
        # scale for 11 bits (signed 12)
        iq = 2**-(self.no_bits - 1) * data.astype(FLOAT)
        return iq.view(COMPLEX)

    def complex2raw(self, data, no_bits):
        iq = np.round((2**(no_bits - 1)) * data.view(FLOAT)).astype(np.int16)
        return iq

    def writeTx(self, data, raw=False):
        rawData = np.array([])
        if len(data) > 0:
            maxBeforeClipping = 15
            dataMax = data.max()
            while np.abs(2**maxBeforeClipping * dataMax > 2**14):
                maxBeforeClipping -= 1
            
            rawData = self.complex2raw(data, maxBeforeClipping + 1) if not raw else data
            # Simulated Channel
            t0 = 0  # channel delay
            A = 2**self.no_bits  # channel gain
            h = A * np.append(np.zeros(t0, dtype=int), [1])

            r = sig.convolve(data, h)
            r = r + 0.4 * np.random.randn(len(r))  # add in noise
            # makes tx cyclical til buffer max size
            repeats = 1.0 * len(self._buffer) / len(r)
            r = np.tile(r, int(np.ceil(repeats)))
            self._buffer = r[0:len(self._buffer)]
        else:
            r = np.zeros(len(self._buffer))
            self._buffer = r[0:len(self._buffer)]

        return len(data), rawData

    def readRx(self, num_samples, raw=False):
        a = np.zeros(num_samples, complex)
        if num_samples > len(self._buffer):
            a[0:len(self._buffer)] = self._buffer
        else:
            a = self._buffer[0:num_samples]

        lastRead = self._lastRead
        self._lastRead = timer()

        # simulate the remaining time required
        # to collect the requested samples
        timeForSamples = (num_samples / self.sampling_frequency / 1e6)
        if self._lastRead - lastRead < timeForSamples:
            time.sleep(timeForSamples - (self._lastRead - lastRead))

        return a / (2**self.no_bits - 1)