
class PACKET_TYPE(object):
    """
    Defines the different packet types available.
    Serves as an enum class
    """
    CONNECTION = 1
    ACK = 2
    DATA = 3

class XIPacketHeader(object):
    """
    Packet Header 
    
    Definition
    -----------

    TYPE (2 bits) | Payload Length (14 bits) | CRC (8 bits)

    """

    def __init__(self, type=PACKET_TYPE.DATA, payloadLength=0):
        """
        Initialize Packet Header.

        params:
            type: type=PACKET_TYPE
                type of packet
            payloadLength: type=int
                length of packet payload
        """
        self.type = type # 2 bits
        self._type_bit_length = 2
        self.payloadLength = payloadLength # 14 bits
        self._payload_length_bit_length = 14

        self.crc = 0 # this will be updated by updateCRC call
        self._crc_bit_length = 8
        self.updateCRC()
    

    def _get_length(self):
        '''
        Gets length in bytes
        '''
        length_in_bits = self._crc_bit_length + self._payload_length_bit_length + self._type_bit_length

        return length_in_bits / 8

    length = property(_get_length)


    def updateCRC(self):
        self.crc = 0xff # crc is set to 0xff to prior to calculation

        self.crc += self.type + self.payloadLength # sum contents of packet header

        self.crc = ~(self.crc % 0xFF) # fit the crc in a byte then perform one's complement



class XIPacket(object):
    """
    Packet 
    
    Definition
    -----------

    Using XIPacketHeader:

    Packet Header (3B) | Payload (Max 16KB)

    """
    def __init__(self, buffer=[]):

        self.header = XIPacketHeader(payloadLength=len(buffer))
        self.payload = bytearray(buffer) # create a buffer of bytes for the payload
        self.length = self.header.length + self.header.payloadLength # length is just the header + packet

    
