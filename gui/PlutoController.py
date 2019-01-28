import iio
import testPlot
import time
from pluto.pluto_sdr import PlutoSdr

sdr = None
rxSamples = 100

def getSdr():
    """
    Gets PlutoSdr object from pluto.pluto_sdr module
    
    returns: type=pluto.pluto_sdr.PlutoSdr
    """
    global sdr
    if sdr is None:
        sdr = PlutoSdr(uri=str(next(enumerate(iio.scan_contexts()))[1]))

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

def plutoRXThread(args):
    global sdr, rxSamples
    while not args['done']:
        # rxData = sdr.readRx(100, False) # Imaginary & Real
        # ys = [ y for i, y in enumerate(rxData) if i % 2 != 0 ] # Imaginary
        # xs = [ x for i, x in enumerate(rxData) if i % 2 == 0 ] # Real
        
        rxData = sdr.readRx(rxSamples) # raw
        ys = [ y for y in rxData ] # time domain samples
        xs = [ t / (sdr.sampling_frequency * 1e6) for t in range(len(rxData)) ] # time domain samples

        testPlot.xs = xs
        testPlot.ys = ys
        time.sleep(0.1)
