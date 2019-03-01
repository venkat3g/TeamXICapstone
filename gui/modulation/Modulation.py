import numpy as np
from filter import srrc
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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

    def _get_pilot_upsample(self):
        return Modulation._upsample(self.pilot_sequence, self.P, float)

    pilot_sequence = property(_get_pilot_sequence)
    _pilot_upsample = property(_get_pilot_upsample)

    def _get_footer_sequence(self):
        # Flip pilot sequence
        return np.flip(self.pilot_sequence)

    def _get_footer_upsample(self):
        return Modulation._upsample(self.footer_sequence, self.P, float)

    footer_sequence = property(_get_footer_sequence)
    _footer_upsample = property(_get_footer_upsample)

    _P = 30
    _D = 4
    _alpha = 0.3

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
            sampling freqency (Hz)
        data : str
            data represented as a string
        Returns
        --------
        1-D ndarray of floats
        """
        # Get Pulse Shaping Filter
        g = self.pulseShapingFilter(self.D, self.alpha, self.P)

        _pilots = self.pilot_sequence # alias
        _footer = self.footer_sequence

        # symbol mapping
        symbols = self.symbolMap(data, False)

        # create packet by concatenating pilots with data
        packet = list(_pilots)
        packet.extend(symbols)
        packet.extend(_footer)

        # upsample packet and convolve packetup with pulse shaping filter g
        m = sig.upfirdn(g, packet, self.P)
        
        return m
    
    def demodulateData(self, fc, fs, rxData, showFinalConstellation=False, showAllPlots=False):
        """
        Demodulates the given data for a given frequency center and sampling frequency.

        Parameeters
        -------------
        fc : int
            center frequency (Hz)
        fs : int
            sampling freqency (Hz)
        rxData : list
            raw data received from rx
        Returns
        --------
        string representation of data
        """
        _pilots = self.pilot_sequence # alias
        g = self.pulseShapingFilter(self.D, self.alpha, self.P)

        # upsample _pilots
        aup = self._pilot_upsample # alias
        footerUp = self._footer_upsample # alias
        
        # convolve demodulated signal with pulse shaping filter
        yup = sig.convolve(rxData, g)
        
        # time framing sync using correlation
        timingTest = sig.convolve(yup, np.flip(aup))
        absTimingTest = np.abs(timingTest)
        peakMag1 = absTimingTest.max()
        peakIndexList1, _ = sig.find_peaks(absTimingTest, np.floor(peakMag1))
        peakStartIndex = peakIndexList1[0]
        
        # footer timing
        timingTestEnd = sig.convolve(yup, np.flip(np.conj(footerUp)))
        timingTestEnd = np.append(np.zeros(peakStartIndex), timingTestEnd[peakStartIndex:]) # start looking after 
        absTimingTestEnd = np.abs(timingTestEnd)
        peakMag2 = absTimingTestEnd.max()
        peakIndexList2, _ = sig.find_peaks(absTimingTestEnd, np.floor(peakMag2))
        peakEndIndex = peakIndexList2[0]
        
        if showAllPlots:
            timingFigure = plt.figure()
            ax = timingFigure.add_subplot(111)
            ax.scatter(range(len(timingTest)), np.abs(timingTest))
            ax.scatter(range(len(timingTestEnd)), np.abs(timingTestEnd))
            ax.set_title('Timing Figure')

        # index of first pilot symbol
        t0 = peakStartIndex - len(aup) + 1

        # index last symbol
        tEnd = peakEndIndex

        # get pilots, data, and footer from upsampled y (footer is ignored)
        yPilots, yData, _ = self._sep_upsampled_data(yup, t0, tEnd, showAllPlots=showAllPlots)
        
        # freq and phase error correction using pilot sequence
        strOut = self._freq_phase_error_correction(fs, yPilots, yData, showFinalConstellation=showFinalConstellation, showAllPlots=showAllPlots)

        if showAllPlots or showFinalConstellation:
            plt.show()

        return strOut
    
    def symbolMap(self, data, raw=False):
        raise NotImplementedError("Call to abstract Modulation Interface or method not yet implemented")
    
    def symbolDemap(self, symbols, raw=False):
        raise NotImplementedError("Call to abstract Modulation Interface or method not yet implemented")

    def _freq_phase_error_correction(self, fs, yPilots, yData, showFinalConstellation=False, showAllPlots=False):
        _pilots = self.pilot_sequence # alias
        
        if len(yPilots) != len(_pilots):
            return ""
        else:
            phaseError = np.unwrap(np.angle(yPilots / _pilots))
            lineFit = np.polyfit(range(len(_pilots)), phaseError, 1)
            slope = lineFit[0]
            intercept = lineFit[1]
            line = slope*np.arange(len(_pilots))+intercept
            if showAllPlots:
                phaseErrorPlot = plt.figure()
                ax = phaseErrorPlot.add_subplot(111)
                ax.plot(range(0, len(_pilots)), line)
                ax.scatter(range(0, len(_pilots)), phaseError)
                ax.set_title('Phase Error')

            # Freq and Phase Offsets
            T = self.P / fs
            f0 = -slope / (2 * np.pi * T) # T or Ts?
            phi = -1 * intercept
            phideg = phi * 180.0 / np.pi

            # Correct for freq and phase offset
            n = np.arange(len(_pilots), (len(yData) + len(_pilots))) # TODO not sure this is always true
            syncData = yData * np.exp(-1.j * (slope * n + intercept))

            # undo symbol mapping
            strOut = self.symbolDemap(syncData, False)
            strOut = "".join([chr(c) for c in strOut])

            # final constellation
            if showFinalConstellation or showAllPlots:
                constellationFigure = plt.figure()
                ax = constellationFigure.add_subplot(111, projection='3d')
                ax.scatter(syncData.real, range(len(syncData)), syncData.imag)
                ax.set_title('Final Constellation')

            return strOut

    def _sep_upsampled_data(self, yup, t0, tEnd, showAllPlots=False):
        _pilots = self.pilot_sequence # alias
        _footer = self.footer_sequence # alias

        y = yup[t0:tEnd:self.P]
        yPilots = y[0:len(_pilots)]
        yData = y[len(_pilots):len(y)-len(_footer)]
        yFooter = y[len(_pilots) + len(yData):]
        if showAllPlots:
            initConstFig = plt.figure()
            ax = initConstFig.add_subplot(111, projection='3d')
            ax.scatter(yData.real, range(len(yData)), yData.imag)
            ax.set_title('Initial Constellation')
        
        return (yPilots, yData, yFooter)

class _BPSK(Modulation):
    '''
    BPSK Modulation implementation.
    '''
    def symbolMap(self, data, raw=False):
        
        binaryRep = _get_binary_rep(data)
        
        symbols = [(int(x) * 2 - 1)+ 0.j for x in binaryRep]

        return symbols

    def symbolDemap(self, rxData, raw=False):
        bits = [str(1 if v.real > 0 else 0) for v in rxData]
        binaryRep = "".join(bits)

        bytes_grouping = [ int(x, 2) for x in _split_by(binaryRep, 8)]

        return bytes_grouping


class _QPSK(Modulation):
    '''
    QPSK Modulation implementation.
    '''
    def symbolMap(self, data, raw=False):
        binaryRep = _get_binary_rep(data)
        groupedBits = _split_by(binaryRep, 2)

        symbols = _QPSK._fit_into_quads(groupedBits)

        return complex2raw(symbols) if raw else np.array(symbols)

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
