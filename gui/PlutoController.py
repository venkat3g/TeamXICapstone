import iio
import testPlot
import time
from pluto.pluto_sdr import PlutoSdr
import numpy as np
from pluto import fir_tools
import scipy.signal as signal
import scipy.fftpack as fftpack


_sdr = None

threadPeriod = 5

rxSamples = 2**16
rxGainModeIndex =  1
rxGainModes = ["manual", "slow_attack", "fast_attack", "hybrid"]
rxPlotList = ["Time", "Frequency", "Constellation (X vs Y)"]
rxPlotIndex = 2

txSamples = 2**15
txDataFile = ""
txPlotList = ["Time", "Frequency", "Constellation (X vs Y)"]
txPlotIndex = 0

def getSdr():
    """
    Gets PlutoSdr object from pluto.pluto_sdr module
    
    returns: type=pluto.pluto_sdr.PlutoSdr
    """
    global _sdr
    if _sdr is None:
        ctxs = iio.scan_contexts()
        if len(ctxs.keys()) > 0:
            _sdr = PlutoSdr(uri=str(next(enumerate(ctxs))[1]))
        else:
            raise Exception("Could not connect to any Pluto Devices.")

    return _sdr

def getIIOContext():
    """
    Gets iio.Context object for PlutoSDR

    returns: type=iio.Context
    """
    return _sdr.ctx

def configure(frequency, sampling_frequency):
    """
    Configures the Pluto's frequency and sampling frequency

    parameters:
        frequency: type=int
            The frequency to set the Pluto's TX and RX (in MHz)
        sampling_frequency: type=int
            The sampling frequency of the Pluto (in MSPS)
    """
    _sdr.rx_lo_freq = frequency
    _sdr.sampling_frequency = sampling_frequency

def writeXSamples(x):
    """
    Write 0 to X bytes to TX

    parameters:
        x: type=int
            the number of samples to write
    """
    N = x


    fc = _sdr.tx_lo_freq
    ts = 1/float(_sdr.sampling_frequency * 1e6)
    t = np.arange(0, N*ts, ts)

    i = np.sin(2*np.pi*t*fc) * 2**10
    q = np.cos(2*np.pi*t*fc) * 2**10
    
    iq = np.empty((i.size + q.size,), dtype=i.dtype)
    iq[0::2] = i
    iq[1::2] = q
    iq = np.int16(iq)

    _sdr.writeTx(iq, True)

    return _sdr.raw2complex(iq)

def writeXComplexSamples(x):
    """
    Write 0 to X complex samples to TX

    parameters:
        x: type=int
            the number of samples to write
    """
    buf = bytearray()
    for x in range(rxSamples * 128 / 8):
        buf.append(0)

    iq = np.frombuffer(buf, np.complex128)

    _sdr.writeTx(iq, False)

def readComplexRX():
    """
    Read Imaginary and Complex RX data
    """    
    rxData = _sdr.readRx(rxSamples, False) # Imaginary & Real
    # ys = [ y.imag for i, y in enumerate(rxData) ] # Imaginary
    # xs = [ x.real for i, x in enumerate(rxData) ] # Real
    return rxData

def readRawRX():
    """
    Read Raw RX data
    """
    rxData = _sdr.readRx(rxSamples, True) # raw
    return rxData

def plutoRXThread(args):
    global _sdr, rxSamples
    while not args['done']:

        txData = writeXSamples(txSamples)

        rxData = readComplexRX()

        # f, Pper_spec = signal.periodogram(ys, 1.0, 'flattop', scaling='spectrum')

        
        testPlot.compl = True
        # testPlot.plot_fir = True
        testPlot.rxData = rxData
        testPlot.txData = txData

        time.sleep(threadPeriod)


def updateGainMode(value):
    _sdr.rx_gain_mode = value

def updateRXPlot(value):
    global rxPlotIndex
    rxPlotIndex = rxPlotList.index(value)

def updateTXPlot(value):
    global txPlotIndex
    txPlotIndex = txPlotList.index(value)
