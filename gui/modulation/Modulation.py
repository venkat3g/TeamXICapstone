import numpy as np

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
    def modulateData(self, data):
        raise NotImplementedError("Call to abstract Modulation Interface or method not yet implemented")

    def demodulateData(self, rxData):
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
    def symbolMap(self, data, raw=True):
        binaryRep = _get_binary_rep(data)
        a1 = _split_by(binaryRep, 2)

        a2 = _QPSK._fit_into_quads(a1)

        return complex2raw(a2) if raw else np.array(a2)

    def symbolDemap(self, rxData, raw=True):
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
