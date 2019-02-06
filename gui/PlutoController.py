import iio
import testPlot
import time
from pluto.pluto_sdr import PlutoSdr
import numpy as np
from pluto import fir_tools


sdr = None
rxSamples = 1000

def getSdr():
    """
    Gets PlutoSdr object from pluto.pluto_sdr module
    
    returns: type=pluto.pluto_sdr.PlutoSdr
    """
    global sdr
    if sdr is None:
        ctxs = iio.scan_contexts()
        if len(ctxs.keys()) > 0:
            sdr = PlutoSdr(uri=str(next(enumerate(ctxs))[1]))
        else:
            raise Exception("Could not connect to any Pluto Devices.")

    return sdr

def getIIOContext():
    """
    Gets iio.Context object for PlutoSDR

    returns: type=iio.Context
    """
    return getSdr().ctx

def configure(frequency, sampling_frequency):
    """
    Configures the Pluto's frequency and sampling frequency

    parameters:
        frequency: type=int
            The frequency to set the Pluto's TX and RX (in MHz)
        sampling_frequency: type=int
            The sampling frequency of the Pluto (in MSPS)
    """
    getSdr().rx_lo_freq = frequency
    getSdr().sampling_frequency = sampling_frequency

def writeXSamples(x):
    """
    Write 0 to X bytes to TX

    parameters:
        x: type=int
            the number of samples to write
    """
    buf = bytearray()
    for x in range(rxSamples * 16 / 8):
        buf.append(0) # forces x to fit in a byte
        buf.append(x % 0xff) # forces x to fit in a byte

    iq = np.frombuffer(buf, np.int16)

    sdr.writeTx(iq, True)

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

    sdr.writeTx(iq, False)

def readImagRealRX():
    """
    Read Imaginary and Complex RX data
    """    
    rxData = sdr.readRx(rxSamples, False) # Imaginary & Real
    ys = [ y.imag for i, y in enumerate(rxData) ] # Imaginary
    xs = [ x.real for i, x in enumerate(rxData) ] # Real
    return (ys, xs)

def readRawRX():
    """
    Read Raw RX data
    """
    rxData = sdr.readRx(rxSamples, True) # raw
    ys = [ y for y in rxData ] # time domain samples
    xs = [ t  for t in range(len(rxData)) ] # sample numbers
    return (ys, xs, rxData)

def plutoRXThread(args):
    global sdr, rxSamples
    while not args['done']:

        (ys, xs, rxData) = readRawRX()

        writeXSamples(rxSamples)

        testPlot.xs = xs
        testPlot.ys = ys
        testPlot.plot_fir = True
        testPlot.rxData = rxData

        time.sleep(0.1)
