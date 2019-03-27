import numpy as np


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

    HEADER (1B) - 0x01 | TYPE (2 bits) 
        | SRC (1 bits) | DST (1 bits) | SEQ NUM (2 bits)
        | Payload Length (10 bits) | CRC (8 bits)

    """

    def __init__(self,
                 type=PACKET_TYPE.DATA,
                 payloadLength=0,
                 src=0,
                 dst=0,
                 seqNum=0):
        """
        Initialize Packet Header.

        params:
            type: type=PACKET_TYPE
                type of packet
            payloadLength: type=int
                length of packet payload
            src: type=int
                source of the message
            dst: type=int
                destination of the message
        """
        self.header = 0x01  # 1 byte
        self._header_bit_length = 8

        self.type = type  # 2 bits
        self._type_bit_length = 2

        self.src = src  # 1 bits
        self._src_bit_length = 1
        self.dst = dst  # 1 bits
        self._dst_bit_length = 1

        self.seqNum = seqNum
        self._seq_num_bit_length = 2

        self.payloadLength = payloadLength  # 10 bits
        self._payload_length_bit_length = 10

        self.crc = 0  # this will be updated by updateCRC call
        self._crc_bit_length = 8
        self.updateCRC()

    def _get_length(self):
        '''
        Gets length in bytes
        '''
        length_in_bits = self._header_bit_length + self._type_bit_length \
                        + self._src_bit_length + self._dst_bit_length \
                        + self._seq_num_bit_length \
                        + self._payload_length_bit_length + self._crc_bit_length

        return length_in_bits / 8

    length = property(_get_length)

    def updateCRC(self):
        self.crc = 0xff  # crc is set to 0xff to prior to calculation

        # sum contents of packet header
        self.crc += self.type
        self.crc += self.payloadLength
        self.crc += self.src
        self.crc += self.dst
        self.crc += self.seqNum

        # fit the crc in a byte then perform one's complement
        self.crc = ~(self.crc % 0xFF) % 0xFF

    def _get_rep(self):
        firstByte = chr(self.header)
        secondByte = 0
        thirdByte = 0
        fourthByte = chr(self.crc)

        # second byte:
        # [type (2b) | src (1b) | dst (1b) | seq (2b) | MSB payload length (2b)]
        secondByte = chr(((self.type & 0b11) << 6) + (
            (self.src & 0b1) << 5) + ((self.dst & 0b1) << 4) + (
                (self.seqNum & 0b11) << 2) + (
                    (self.payloadLength & 0x300) >> 8))
        # third byte:
        # [LSB payload length (8b)]
        thirdByte = chr(self.payloadLength & 0xFF)

        return "".join([firstByte, secondByte, thirdByte, fourthByte])

    @staticmethod
    def createXIPacketHeader(buffer):
        """
        Creates a XI Packet Header using a buffer that begins
        with a valid XIPacketHeader.

        params:
            buffer: type=str

        returns:
            None if buffer does not contain a
            valid XIPacketHeader.
            Or returns a valid XIPacketHeader.
        """
        if len(buffer) < 4:
            return None

        header = XIPacketHeader()
        firstByte = ord(buffer[0])
        secondByte = ord(buffer[1])
        thirdByte = ord(buffer[2])
        fourthByte = ord(buffer[3])

        # second byte:
        # [type (2b) | src (1b) | dst (1b) | seq (2b) | MSB payload length (2b)]
        _type = (secondByte >> 6) & 0b11
        src = (secondByte >> 5) & 0b1
        dst = (secondByte >> 4) & 0b1
        seqNum = (secondByte >> 2) & 0b11
        payloadLength = (secondByte & 0b11) << 8

        # third byte:
        # [LSB payload length (8b)]
        payloadLength += thirdByte

        crc = fourthByte

        header.type = _type
        header.src = src
        header.dst = dst
        header.seqNum = seqNum
        header.payloadLength = payloadLength
        header.updateCRC()

        if firstByte != 0x1 or header.crc != crc:
            header = None

        return header

    rep = property(_get_rep)


class XIPacket(object):
    """
    Packet 
    
    Definition
    -----------

    Using XIPacketHeader:

    Packet Header (4B) | Payload (Max 1KB-1B) | CRC (1B) | Packet Footer 0x13 (1B)

    """

    def __init__(self, buffer="", type=PACKET_TYPE.DATA, seqNum=0):

        self.header = XIPacketHeader(
            payloadLength=len(buffer), type=type, seqNum=seqNum)
        self.payload = buffer
        self.crc = 0
        self.footer = 0x13

        self.updateCRC()

    def updateCRC(self):
        self.crc = 0xff

        # sum all bytes
        for b in self.payload:
            if isinstance(b, str):
                self.crc += ord(b)

        # fit the crc in a byte then perform one's complement
        self.crc = ~(self.crc % 0xFF) % 0xFF

    def _get_length(self):
        # 2 bytes at the end, 1 for the CRC and 1 for 0x13 packet footer
        return self.header.length + self.header.payloadLength + 2

    length = property(_get_length)

    def _get_rep(self):
        rep = []
        rep.append(self.header.rep)
        rep.extend(self.payload)
        rep.append(chr(self.crc))
        rep.append(chr(self.footer))

        return "".join(rep)

    rep = property(_get_rep)

    def __eq__(self, other):
        strRep = None
        if isinstance(other, str):
            strRep = other
        elif isinstance(other, XIPacket):
            strRep = other.rep
        return self.rep == strRep

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.rep)


    @staticmethod
    def createXIPacket(buffer):
        """
        Creates a XI Packet using a buffer that begins
        with a valid XIPacketHeader.

        params:
            buffer: type=str

        returns:
            None if buffer does not contain a
            valid XIPacket.
            Or returns a valid XIPacket.
        """
        packet = None
        header = XIPacketHeader.createXIPacketHeader(buffer)

        if header != None:
            payloadOffset = header.length
            payloadLength = header.payloadLength
            crcOffset = payloadOffset + payloadLength
            footerOffset = crcOffset + 1

            # the expected size is the header + payload + crc + footer
            expectedSize = header.length + payloadLength + 2

            # buffer must be at least the expected size
            # as it may contain noise after footer.
            if len(buffer) >= expectedSize:
                packet = XIPacket()
                packet.header = header
                packet.payload = buffer[payloadOffset:payloadOffset +
                                        payloadLength]
                crc = ord(buffer[crcOffset:crcOffset + 1])
                packet.footer = ord(buffer[footerOffset:footerOffset + 1])

                packet.updateCRC()

                if crc != packet.crc or packet.footer != 0x13:
                    packet = None

        return packet

    @staticmethod
    def maxPayload():
        return 2**(XIPacketHeader()._payload_length_bit_length) - 1
