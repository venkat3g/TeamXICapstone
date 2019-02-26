import iio
import testPlot
import time
from pluto.pluto_sdr import PlutoSdr
import numpy as np
from pluto import fir_tools
import scipy.signal as signal
import scipy.fftpack as fftpack
from modulation.Modulation import ModulationFactory


_sdr = None

_scheme = ModulationFactory.chooseScheme(ModulationFactory.QAM)

threadPeriod = 5

rxSamples = 2**14
rxGainModeIndex =  0
rxGainModes = ["manual", "slow_attack", "fast_attack", "hybrid"]
rxPlotList = ["Time", "Frequency", "Constellation (X vs Y)"]
rxPlotIndex = 2

txSamples = 2**15
txDataFile = ""
txPlotList = ["Time", "Frequency", "Constellation (X vs Y)"]
txPlotIndex = 2

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
    raw = False

    # iq = generateRandomWaveform(x)
    # raw = True

    

    msg = "hello world"
    iq = _scheme.modulateData(_sdr.tx_lo_freq, _sdr.sampling_frequency, msg)

    _sdr.writeTx(iq, raw)

    return _sdr.raw2complex(iq) if raw else iq

def generateRandomWaveform(x):
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

    return iq

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


def updateRXImaginary(value):
    testPlot.rxImaginary = value == '1'

def updateTXImaginary(value):
    testPlot.txImaginary = value == '1'

def getRXImaginary():
    return '1' if testPlot.rxImaginary else '0'

def getTXImaginary():
    return '1' if testPlot.txImaginary else '0'

def updateGainMode(value):
    _sdr.rx_gain_mode = value

def updateRXPlot(value):
    global rxPlotIndex
    rxPlotIndex = rxPlotList.index(value)

def updateTXPlot(value):
    global txPlotIndex
    txPlotIndex = txPlotList.index(value)

def updateModScheme(value):
    global _scheme
    _scheme = ModulationFactory.chooseScheme(value)