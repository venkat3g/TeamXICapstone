import iio
import testPlot
import time
from pluto.pluto_sdr import PlutoSdr
import numpy as np
from pluto import fir_tools
import scipy.signal as signal
import scipy.fftpack as fftpack
from modulation.Modulation import ModulationFactory
from plutoDevice.PlutoSdrWrapper import PlutoSdrWrapper
from plutoDevice.SimPlutoSdr import SimPlutoSdr


_sdr = None

_msg = "hello world"
_msg_sent = False
_scheme = ModulationFactory.chooseScheme(ModulationFactory.QAM)
_D = _scheme.D
_P = _scheme.P
_alpha = _scheme.alpha

threadPeriod = 5

rxSamples = 2**14
rxGainModeIndex =  0
rxGainModes = ["manual", "slow_attack", "fast_attack", "hybrid"]
rxPlotList = ["Time", "Frequency", "Constellation (X vs Y)"]
rxPlotIndex = 2
rx_show_all_plots = False

_tx_on = True
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
            _sdr = PlutoSdrWrapper()
        else:
            _sdr = SimPlutoSdr()

    return _sdr

def getIIOContext():
    """
    Gets iio.Context object for PlutoSDR

    returns: type=iio.Context
    """
    return _sdr.ctx

def configure(frequency, sampling_frequency, gain):
    """
    Configures the Pluto's frequency and sampling frequency

    parameters:
        frequency: type=int
            The frequency to set the Pluto's TX and RX (in MHz)
        sampling_frequency: type=int
            The sampling frequency of the Pluto (in MHz)
    """
    getSdr().rx_lo_freq = frequency
    getSdr().tx_lo_freq = frequency
    getSdr().sampling_frequency = sampling_frequency
    getSdr().rx_gain_mode = rxGainModes[0]
    getSdr().rx_gain = 10

def writeXSamples():
    """
    Write 0 to X bytes to TX
    """
    global _msg, _msg_sent
    msg = _msg
    iq = _scheme.modulateData(_sdr.tx_lo_freq, _sdr.sampling_frequency, msg)

    _sdr.writeTx(iq, raw)
    
    _msg_sent = True

    return _sdr.raw2complex(iq) if raw else iq

def turnOffTX():
    _sdr.writeTx([]) # turns off TX

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
    global _sdr, rxSamples, _msg_sent, rx_show_all_plots
    while not args['done']:

        if not _msg_sent and getTXStatus():
            txData = writeXSamples()

        rxData = readComplexRX()
        testPlot.compl = True
        # testPlot.plot_fir = True
        testPlot.rxData = rxData

        if rx_show_all_plots:
            strOut = _scheme.demodulateData(_sdr.rx_lo_freq, _sdr.sampling_frequency, 
                        rxData, showAllPlots=rx_show_all_plots)
            print(len(strOut))
            print(strOut)
        testPlot.txData = txData

        time.sleep(threadPeriod)

def setTXStatus(txOn):
    global _tx_on, _msg_sent
    _tx_on = txOn == '1'

    if not _tx_on:
        turnOffTX()
        _msg_sent = False # Message will be sent again when enabled.

def getTXStatus():
    return _tx_on

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

    if _D is not None:
        _scheme.D = _D
    if _P is not None:
        _scheme.P = _P
    if _alpha is not None:
        _scheme.alpha = _alpha

def updatePulseShapingFilter(D, P, alpha):
    global _D, _P, _alpha, _msg_sent
    _D = D
    _P = P
    _alpha = alpha

    _scheme.D = _D
    _scheme.P = _P
    _scheme.alpha = _alpha
    _msg_sent = False # Message must be resent with new values

def getPulseShapingValues():
    global _D, _P, _alpha
    return (_D, _P, _alpha)

def updateMsgToSend(filename):
    global _msg, _msg_sent, txDataFile
    txDataFile = filename
    if filename is not "":
        _msg = ""
        _msg_sent = False
        with open(filename) as f:
            for x in f:
                _msg += x