import unittest
import xi

class TestXIPacketHeader(unittest.TestCase):

    def test_init(self):
        self.assertNotEqual(xi.XIPacketHeader(), None)

    def test_crc_default(self):
        header1 = xi.XIPacketHeader()
        header2 = xi.XIPacketHeader()
        self.assertEqual(header1.crc, header2.crc)

        header1 = xi.XIPacketHeader(type=xi.PACKET_TYPE.CONNECTION)
        header2 = xi.XIPacketHeader(type=xi.PACKET_TYPE.CONNECTION)
        self.assertEqual(header1.crc, header2.crc)

        header1 = xi.XIPacketHeader(type=xi.PACKET_TYPE.ACK)
        header2 = xi.XIPacketHeader(type=xi.PACKET_TYPE.ACK)
        self.assertEqual(header1.crc, header2.crc)

        header1 = xi.XIPacketHeader(type=xi.PACKET_TYPE.DATA)
        header2 = xi.XIPacketHeader(type=xi.PACKET_TYPE.DATA)
        self.assertEqual(header1.crc, header2.crc)
    
    def test_crc_different_headers(self):
        header1 = xi.XIPacketHeader(type=xi.PACKET_TYPE.ACK, payloadLength=0)
        header2 = xi.XIPacketHeader(type=xi.PACKET_TYPE.CONNECTION, payloadLength=0)
        header3 = xi.XIPacketHeader(type=xi.PACKET_TYPE.DATA, payloadLength=0)

        self.assertNotEqual(header1.crc, header2.crc)
        self.assertNotEqual(header1.crc, header3.crc)
        self.assertNotEqual(header2.crc, header3.crc)

        header1 = xi.XIPacketHeader(type=xi.PACKET_TYPE.CONNECTION, payloadLength=300)
        header2 = xi.XIPacketHeader(type=xi.PACKET_TYPE.CONNECTION, payloadLength=3)
        header3 = xi.XIPacketHeader(type=xi.PACKET_TYPE.CONNECTION, payloadLength=2)

        self.assertNotEqual(header1.crc, header2.crc)
        self.assertNotEqual(header1.crc, header3.crc)
        self.assertNotEqual(header2.crc, header3.crc)

class TestXIPacket(unittest.TestCase):

    def test_init(self):
        self.assertNotEqual(xi.XIPacket(), None)

    def test_empty_packet(self):
        packet1 = xi.XIPacket()
        packet2 = xi.XIPacket()

        # the packet length should equal the size of the packet header
        self.assertEqual(packet1.length, packet1.header.length)

        # two empty packets should have the same size
        self.assertEqual(packet1.length, packet2.length)

        # empty packet should have a payload length of zero in the packet header
        self.assertEqual(len(packet1.payload), 0)
        self.assertEqual(packet1.header.payloadLength, 0)

    def test_packet_w_valid_buffer(self):
        payloadLength = 1000
        packet1 = xi.XIPacket(buffer=[x % 0xFF for x in range(payloadLength)])

        self.assertEqual(len(packet1.payload), payloadLength)
        self.assertEqual(packet1.header.payloadLength, payloadLength)
        self.assertEqual(packet1.length, packet1.header.length + packet1.header.payloadLength)

    def test_packet_w_invalid_buffer(self):
        payloadLength = 1000

        # buffer must contain an array of bytes, therefore values must be in range(256)
        with self.assertRaises(ValueError):
            xi.XIPacket(buffer=[x for x in range(payloadLength)])



if __name__ == '__main__':
    unittest.main()