from pluto.pluto_sdr import PlutoSdr
import numpy as np
import logging
import iio

class PlutoSdrWrapper(PlutoSdr):
    """
    This is a wrapper class aimed at fixing any potential \
    bugs found in PlutoSdr. This wrapper class will also \
    attempt to ease any potentially long or repetitive \
    operations.
    """
    def __init__(self):
        """
        Will pick the first available iio context. \
        Note: this assumes that the first context \
        is a Pluto Device.
        """
        contexts = iio.scan_contexts()
        if len(contexts.keys()) > 0:
            uri = str(next(enumerate(contexts))[1])
            PlutoSdr.__init__(self, uri=uri)
        else:
            raise Exception("Could not find any Pluto Devices")


    def writeTx(self, samples): #, raw=False): use samples.dtype
        """
        Attempts to fix a bug found in writeTx in PlutoSdr.


        Write to the Tx buffer and make it cyclic
        """
        if self._tx_buff is not None:
            self._tx_buff = None               # turn off any previous signal
        if not(isinstance(samples, np.ndarray)):          
            logging.debug('tx: off')           # leave with transmitter off
            self.tx_state = self.TX_OFF
            return
        if samples.dtype==np.int16:
            data = samples<<4         # align 12 bit raw to msb
        else:   # samples can come from some DiscreteSignalSource, if so
                # data is complex IQ and scaled to +/-1.0 float range
                # use 16 **not** self.no_bits to align data to msb
            data = self.complex2raw(samples, 12)
        # samples are 2 bytes each with interleaved I/Q value (no_samples = len/4)
        self.tx_state = self.TX_DMA                 # enable the tx channels
        try:  # create a cyclic iio buffer for continuous tx output
            self._tx_buff = iio.Buffer(self.dac, len(data)//2, True)
            count = self._tx_buff.write(np.frombuffer(data, np.uint8))
            logging.debug(str(count)+' samples transmitted')
            self._tx_buff.push()
        except OSError:
            self.tx_state = self.TX_OFF
            raise OSError('failed to create an iio buffer')
        # buffer retained after a successful call
        return count, data # just for now