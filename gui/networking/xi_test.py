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
        header2 = xi.XIPacketHeader(
            type=xi.PACKET_TYPE.CONNECTION, payloadLength=0)
        header3 = xi.XIPacketHeader(type=xi.PACKET_TYPE.DATA, payloadLength=0)

        self.assertNotEqual(header1.crc, header2.crc)
        self.assertNotEqual(header1.crc, header3.crc)
        self.assertNotEqual(header2.crc, header3.crc)

        header1 = xi.XIPacketHeader(
            type=xi.PACKET_TYPE.CONNECTION, payloadLength=300)
        header2 = xi.XIPacketHeader(
            type=xi.PACKET_TYPE.CONNECTION, payloadLength=3)
        header3 = xi.XIPacketHeader(
            type=xi.PACKET_TYPE.CONNECTION, payloadLength=2)

        self.assertNotEqual(header1.crc, header2.crc)
        self.assertNotEqual(header1.crc, header3.crc)
        self.assertNotEqual(header2.crc, header3.crc)

    def test_create_header(self):
        # tests the .rep property to ensure that
        # a new XIPacketHeader can be created by
        # the string rep of an existing header.
        header1 = xi.XIPacketHeader(type=xi.PACKET_TYPE.ACK, payloadLength=0)
        header2 = xi.XIPacketHeader.createXIPacketHeader(header1.rep)

        self.assertEqual(header1.rep, header2.rep)

        header1 = xi.XIPacketHeader(
            type=xi.PACKET_TYPE.DATA, payloadLength=xi.XIPacket.maxPayload())
        header2 = xi.XIPacketHeader.createXIPacketHeader(header1.rep)

        self.assertEqual(header1.rep, header2.rep)

        header1 = xi.XIPacketHeader(
            type=xi.PACKET_TYPE.CONNECTION, payloadLength=2**2)
        header2 = xi.XIPacketHeader.createXIPacketHeader(header1.rep)

        self.assertEqual(header1.rep, header2.rep)

    def test_bad_header(self):
        # tests the .rep property to ensure that
        # a new XIPacketHeader can be created by
        # the string rep of an existing header.
        badHeader = ""
        header = xi.XIPacketHeader.createXIPacketHeader(badHeader)

        badHeader = "".join([chr(0), chr(0), chr(0), chr(0)])
        header = xi.XIPacketHeader.createXIPacketHeader(badHeader)

        self.assertIsNone(header)

    def test_non_default_values(self):
        srcBits = xi.XIPacketHeader()._src_bit_length
        dstBits = xi.XIPacketHeader()._dst_bit_length
        seqNumBits = xi.XIPacketHeader()._seq_num_bit_length

        # test all possible type, src, dst, seq num combinations
        for _type in [
                xi.PACKET_TYPE.ACK, xi.PACKET_TYPE.CONNECTION,
                xi.PACKET_TYPE.DATA
        ]:
            for src in range(2**srcBits):
                for dst in range(2**dstBits):
                    for seqNum in range(2**seqNumBits):
                        header1 = xi.XIPacketHeader(
                            type=_type,
                            payloadLength=0,
                            seqNum=seqNum,
                            src=src,
                            dst=dst)
                        header2 = xi.XIPacketHeader.createXIPacketHeader(
                            header1.rep)

                        self.assertEqual(header1.rep, header2.rep)


class TestXIPacket(unittest.TestCase):
    def test_init(self):
        self.assertNotEqual(xi.XIPacket(), None)

    def test_empty_packet(self):
        packet1 = xi.XIPacket()
        packet2 = xi.XIPacket()

        # two empty packets should have the same size
        self.assertEqual(packet1.length, packet2.length)

        # empty packet should have a payload length of zero in the packet header
        self.assertEqual(len(packet1.payload), 0)
        self.assertEqual(packet1.header.payloadLength, 0)

    def test_packet_w_valid_buffer(self):
        payloadLength = 1000
        packet1 = xi.XIPacket(
            buffer="".join([chr(x % 0xFF) for x in range(payloadLength)]))

        self.assertEqual(len(packet1.payload), payloadLength)
        self.assertEqual(packet1.header.payloadLength, payloadLength)
        self.assertGreaterEqual(packet1.crc, 0)
        self.assertLessEqual(packet1.crc, 255)

        self.assertGreaterEqual(packet1.header.crc, 0)
        self.assertLessEqual(packet1.header.crc, 255)

    def test_packet_w_str_buffer(self):
        packet1 = xi.XIPacket(buffer="hello world")
        payloadLength = len(packet1.payload)

        self.assertEqual(len(packet1.payload), payloadLength)
        self.assertEqual(packet1.header.payloadLength, payloadLength)
        self.assertGreaterEqual(packet1.crc, 0)
        self.assertLessEqual(packet1.crc, 255)

        self.assertGreaterEqual(packet1.header.crc, 0)
        self.assertLessEqual(packet1.header.crc, 255)

    def test_create_header(self):
        # tests the .rep property to ensure that
        # a new XIPacket can be created by the string rep
        # of an existing XIPacket.
        packet1 = xi.XIPacket()
        packet2 = xi.XIPacket.createXIPacket(packet1.rep)

        self.assertEqual(packet1.rep, packet2.rep)

    def test_crc(self):
        payloadLength = 1000
        packet1 = xi.XIPacket(
            buffer="".join([chr(x % 0xFF) for x in range(payloadLength)]))
        packet2 = xi.XIPacket(
            buffer="".join([chr(x % 0xFF) for x in range(payloadLength)]))

        self.assertEqual(packet1.header.payloadLength,
                         packet2.header.payloadLength)
        self.assertEqual(packet1.header.crc, packet2.header.crc)
        self.assertEqual(packet1.crc, packet2.crc)

    def test_packet_creation(self):
        payloadLength = xi.XIPacket.maxPayload()
        packet1 = xi.XIPacket(
            buffer="".join([chr(x % 0xFF) for x in range(payloadLength)]))
        packet2 = xi.XIPacket.createXIPacket(packet1.rep)

        self.assertEqual(packet1.rep, packet2.rep)

        packet1 = xi.XIPacket(buffer="Hello World")
        packet2 = xi.XIPacket.createXIPacket(packet1.rep)

        self.assertEqual(packet1.rep, packet2.rep)

    def test_bad_packet_creation(self):
        payloadLength = xi.XIPacket.maxPayload()
        packet1 = xi.XIPacket(
            buffer="".join([chr(x % 0xFF) for x in range(payloadLength)]))

        # act as though the message was interrupted
        packet2 = xi.XIPacket.createXIPacket(packet1.rep[0:payloadLength / 2])

        self.assertIsNone(packet2)

    def test_non_default_values(self):
        seqNumBits = xi.XIPacketHeader()._seq_num_bit_length

        # test all possible type, src, dst, seq num combinations
        for _type in [
                xi.PACKET_TYPE.ACK, xi.PACKET_TYPE.CONNECTION,
                xi.PACKET_TYPE.DATA
        ]:
            for seqNum in range(2**seqNumBits):
                payloadLength = xi.XIPacket.maxPayload()
                packet1 = xi.XIPacket(
                    type=_type,
                    seqNum=seqNum,
                    buffer="".join(
                        [chr(x % 0xFF) for x in range(payloadLength)]))
                packet2 = xi.XIPacket.createXIPacket(packet1.rep)

                self.assertEqual(packet1.rep, packet2.rep)


if __name__ == '__main__':
    unittest.main()