import numpy as np
from filter import srrc
import matplotlib.pyplot as plt
from scipy import signal as sig

def complex2raw(data, no_bits=16):
    iq = np.round((2**(no_bits-1))*np.array(data).view(np.float64)).astype(np.int16)
    return iq

def raw2complex(data):
    """return a scaled complex float version of the raw data"""
    # convert to float64, view performs an in place recast of the data
    # from SO 5658047
    # are the #bits available from some debug attr?
    # scale for 11 bits (signed 12)
    no_bits=16
    iq = 2**-(no_bits-1)*data.astype(np.float64)
    return iq.view(np.complex128)

class Modulation:

    @staticmethod
    def _upsample(a, P, dtype):
        """
        Upsample a given array using the given oversampling factor
        
        Parameters
        ----------
        a : list
            array of data to upsample
        P : int
            factor to oversample by
        dtype:
            type of data
        """
        aup = np.zeros(len(a) * P, dtype=dtype)
        _index_a = 0
        for x in range(0, len(aup), P):
            aup[x] = a[_index_a]
            _index_a += 1

        return aup
    
    def pulseShapingFilter(self, D, alpha, P):
        """
        Generates a pulse shaping filter for our modulation.
        This can be overridden by child classes.
        Parameters
        ----------
        D : int
            Half-length of the pulse
        alpha : float
            Roll off factor (Valid values are [0, 1]).
        P : int
            Oversampling factor (how many samples in-between - 1)

        Returns
        ---------
        1-D ndarray of floats
        """
        return srrc(D, alpha, P)

    def _get_pilot_sequence(self):
        # Pilot Sequence - Barker code
        return [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]

    def _pilot_upsample(self):
        return Modulation._upsample(self.pilot_sequence, self.P, float)

    pilot_sequence = property(_get_pilot_sequence)
    _pilot_upsample = property(_pilot_upsample)

    _P = 110
    _D = 4
    _alpha = 0.1

    def _get_P(self):
        return self._P

    def _get_D(self):
        return self._D

    def _get_alpha(self):
        return self._alpha
    
    def _set_P(self, value):
        self._P = value

    def _set_D(self, value):
        self._D = value

    def _set_alpha(self, value):
        self._alpha = value

    P = property(_get_P, _set_P)
    D = property(_get_D, _set_D)
    alpha = property(_get_alpha, _set_alpha)

    def modulateData(self, fc, fs, data):
        """
        Modulates the given data for a given frequency center and sampling frequency.

        Parameeters
        -------------
        fc : int
            center frequency (Hz)
        fs : int
            sampling freqency (Hz or SPS)
        data : str
            data represented as a string
        Returns
        --------
        1-D ndarray of floats
        """
        Ts = 1.0 / fs

        # Get Pulse Shaping Filter
        
        g = self.pulseShapingFilter(self.D, self.alpha, self.P)

        _pilots = self.pilot_sequence # alias

        # symbol mapping
        symbols = self.symbolMap(data, False)

        # create packet by concatenating pilots with data
        packet = list(_pilots)
        packet.extend(symbols)

        # upsample packet and convolve packetup with pulse shaping filter g
        m = sig.upfirdn(g, packet, self.P)
        
        return m
    
    def demodulateData(self, fc, fs, rxData, showConstellation=False):
        """
        Demodulates the given data for a given frequency center and sampling frequency.

        Parameeters
        -------------
        fc : int
            center frequency (Hz)
        fs : int
            sampling freqency (Hz or SPS)
        rxData : list
            raw data received from rx
        Returns
        --------
        string representation of data
        """
        Ts = 1.0 / fs
        _pilots = self.pilot_sequence # alias
        g = self.pulseShapingFilter(self.D, self.alpha, self.P)

        # upsample _pilots
        a = list(_pilots) # copy list
        aup = self._pilot_upsample # alias
        
        # TODO revisit hardware should handle this demodulation stage.... apparently
        # fOff = 7 # frequency offset of oscillator
        # phiOff = 0.4 # phase offset of oscillator

        # # demodulate w/ freq and phase offset
        # t_v = np.arange(0, len(rxData) * Ts, Ts)
        # v = 2*rxData*np.exp(-1.j*(2*np.pi*(fc+fOff)*t_v+phiOff))

        # convolve demodulated signal with pulse shaping filter
        yup = sig.convolve(rxData, g)
        
        # time framing sync using correlation
        timingTest = sig.convolve(yup, np.flip(aup))
        absTimingTest = np.abs(timingTest)
        peakMag = absTimingTest.max()
        peakIndex = np.argmax(absTimingTest)

        # index of first pilot symbol
        t0 = peakIndex - len(aup) + 1

        # get pilots and data from upsampled y
        y = yup[t0:t0 + (len(yup) - len(aup)) - 1:self.P] # TODO not sure is always true
        yPilots = y[0:len(_pilots)]
        yData = y[len(_pilots):]
        
        # freq and phase error correction
        phaseError = np.unwrap(np.angle(yPilots / a))
        lineFit = np.polyfit(range(len(_pilots)), phaseError, 1)
        slope = lineFit[0]
        intercept = lineFit[1]
        line = slope*np.arange(len(_pilots))+intercept

        # Freq and Phase Offsets
        T = self.P / fs
        f0 = -slope / (2 * np.pi * T) # T or Ts?
        phi = -1 * intercept
        phideg = phi * 180.0 / np.pi

        # Correct for freq and phase offset
        n = np.arange(len(_pilots), (len(yData) + len(_pilots))) # TODO not sure this is always true
        syncData = yData * np.exp(-1.j * (slope * n + intercept))

        # final constellation
        if showConstellation:
            plt.scatter(syncData.real, syncData.imag)
            plt.show()

        # undo symbol mapping
        strOut = self.symbolDemap(syncData[:len(syncData) - (len(syncData) % 8)], False)
        return "".join([chr(c) for c in strOut])
    
    def symbolMap(self, data, raw=False):
        raise NotImplementedError("Call to abstract Modulation Interface or method not yet implemented")
    
    def symbolDemap(self, symbols, raw=False):
        raise NotImplementedError("Call to abstract Modulation Interface or method not yet implemented")

 
class _BPSK(Modulation):
    '''
    BPSK Modulation implementation.
    '''
    def symbolMap(self, data):
        
        binaryRep = _get_binary_rep(data)
        
        a = [(int(x) * 2 - 1)+ 0.j for x in binaryRep]

        return complex2raw(a)


class _QPSK(Modulation):
    '''
    QPSK Modulation implementation.
    '''
    def symbolMap(self, data, raw=False):
        binaryRep = _get_binary_rep(data)
        a1 = _split_by(binaryRep, 2)

        a2 = _QPSK._fit_into_quads(a1)

        return complex2raw(a2) if raw else np.array(a2)

    def symbolDemap(self, rxData, raw=False):
        data = raw2complex(rxData) if raw else rxData

        # take complex data and group it into
        # 00, 01, 10, 11
        labels = [str(1 if x.real >= 0 else 0) + str(1 if x.imag >= 0 else 0) for x in data]
        
        binaryRep = "".join(labels)

        bytes_grouping = [ int(x, 2) for x in _split_by(binaryRep, 8)]

        return bytes_grouping

    @staticmethod
    def _fit_into_quads(a1):
        a2 = []
        for i in a1:
            if i == '00':
                a2.append( (-1-1.j) / 2**0.5 )
            elif i == '01':
                a2.append( (-1+1.j) / 2**0.5 )
            elif i == '10':
                a2.append( (1-1.j) / 2**0.5 )
            elif i == '11':
                a2.append( (1+1.j) / 2**0.5 )
            else:
                raise ValueError("Unexpected Value")
        return a2

def _get_binary_rep(data):
    binaryRep = ""
    for v in bytearray(data): 
        binaryRep += format(v, '#010b')[2::]
    return binaryRep

def _split_by(binaryRep, value):
    a1 = []
    i = 0
    while i < len(binaryRep) - 1:
        s = ""
        for j in range(value):
            s += binaryRep[i + j]
        a1.append(s)
        i += value

    return a1

class ModulationFactory:
    BPSK = 'bpsk'
    QPSK = 'qpsk'
    QAM = 'qam'
    SUPPORTED_SCHEMES = [BPSK, QPSK, QAM]

    @staticmethod
    def chooseScheme(scheme, **args):
        '''
        Choose a supported modulation scheme.
        
        params:
        scheme: type=str
            The name of the scheme

        **args: type=dict
            Arguments for the specific modulation scheme.
            If arguments are not specified defaults will be chosen.

        returns: type=Modulation
            the modulation instance
        '''
        if scheme == ModulationFactory.BPSK:
            return _create_bpsk_modulation(args=args)
        elif scheme == ModulationFactory.QAM or scheme == ModulationFactory.QPSK:
            return _create_qam_modulation(args=args)
        else:
            raise ValueError(scheme + ' is not supported')

def _create_bpsk_modulation(**args):
    return _BPSK()

def _create_qam_modulation(**args):
    return _QPSK()
