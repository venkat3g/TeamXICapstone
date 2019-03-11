import unittest
from timeit import default_timer as timer
from Modulation import Modulation, ModulationSettings, ModulationFactory
from ..networking.xi import XIPacket
import filter as f
import numpy as np


class TestModulationSettings(unittest.TestCase):
    def test_init(self):
        self.assertIsNotNone(ModulationSettings)

        scheme = ModulationFactory.chooseScheme('qam')
        settings = ModulationSettings(scheme)
        self.assertIsNotNone(settings)
        self.assertIsInstance(settings, ModulationSettings)
        self.assertIsInstance(settings.getString(), str)

    def test_modulation_creation(self):
        msg = 'hello world'
        scheme = ModulationFactory.chooseScheme('qam')
        settings = ModulationSettings(scheme)
        scheme2 = ModulationSettings.createModulation(settings.getString())

        schemeMod = scheme.modulateData(msg)
        scheme2Mod = scheme2.modulateData(msg)
        self.assertTrue(np.array_equal(schemeMod, scheme2Mod))

        schemeDemod = scheme.demodulateData(schemeMod)
        scheme2Demod = scheme2.demodulateData(schemeMod)
        self.assertEqual(schemeDemod, scheme2Demod)

        schemeDemod = scheme.demodulateData(scheme2Mod)
        scheme2Demod = scheme2.demodulateData(scheme2Mod)
        self.assertEqual(schemeDemod, scheme2Demod)


class TestModulationFactory(unittest.TestCase):
    def test_init(self):
        self.assertIsNotNone(ModulationFactory)


class TestModulation(unittest.TestCase):
    def test_init(self):
        self.assertIsNotNone(Modulation())


class TestQPSK(unittest.TestCase):

    scheme = ModulationFactory.chooseScheme('qpsk')

    def test_init(self):
        self.assertIsNotNone(ModulationFactory.chooseScheme('qpsk'))
        self.assertIsNotNone(
            ModulationFactory.chooseScheme(ModulationFactory.QPSK))

    def test_create_symbol(self):
        msg = 'abc'
        msg2 = 'hello world'

        self.assertIsNotNone(self.scheme.symbolMap(msg))
        self.assertIsNotNone(self.scheme.symbolMap(msg2))

        # tests that the buffer is the exact same when given two identical messages
        tx_buf = self.scheme.symbolMap(msg)
        tx_buf2 = self.scheme.symbolMap(msg)
        self.assertTrue(np.array_equal(tx_buf, tx_buf2))

        tx_buf = self.scheme.symbolMap(msg2)
        tx_buf2 = self.scheme.symbolMap(msg2)
        self.assertTrue(np.array_equal(tx_buf, tx_buf2))

        # test that the buffers are not the exact same when given two different messages
        tx_buf = self.scheme.symbolMap(msg)
        tx_buf2 = self.scheme.symbolMap(msg2)
        self.assertFalse(np.array_equal(tx_buf, tx_buf2))

        tx_buf = self.scheme.symbolMap(msg2)
        tx_buf2 = self.scheme.symbolMap(msg)
        self.assertFalse(np.array_equal(tx_buf, tx_buf2))

    def test_timing(self):
        largeMsg = [chr(ord('a') + (x % 26)) for x in range(int(2**10))]
        largerMsg = [chr(ord('a') + (x % 26)) for x in range(int(2**12))]

        start = timer()
        tx_buf = self.scheme.modulateData(largeMsg)
        end = timer()
        print("Large tx buffer creation time: %fus" % ((end - start) * 1e6))

        start = timer()
        tx_buf2 = self.scheme.modulateData(largerMsg)
        end = timer()
        print(
            "Very large tx buffer creation time: %fus" % ((end - start) * 1e6))

        start = timer()
        self.scheme.demodulateData(tx_buf)
        end = timer()
        print("Large rx buffer read time: %fus" % ((end - start) * 1e6))

        start = timer()
        self.scheme.demodulateData(tx_buf2)
        end = timer()
        print("Very large rx buffer read time: %fus" % ((end - start) * 1e6))

    def test_create_read_symbol(self):
        msg = 'abc'
        msg2 = 'hello world'

        tx_buf = self.scheme.symbolMap(msg)
        tx_buf2 = self.scheme.symbolMap(msg2)

        rx_rec_msg = self.scheme.symbolDemap(tx_buf)
        rx_rec_msg2 = self.scheme.symbolDemap(tx_buf2)

        self.assertIsNotNone(rx_rec_msg)
        self.assertIsNotNone(rx_rec_msg2)

        rx_constructed_msg = "".join([chr(x) for x in rx_rec_msg])
        rx_constructed_msg2 = "".join([chr(x) for x in rx_rec_msg2])

        self.assertEqual(rx_constructed_msg, msg)
        self.assertEqual(rx_constructed_msg2, msg2)

        self.assertNotEqual(rx_constructed_msg, rx_constructed_msg2)
        self.assertNotEqual(rx_constructed_msg, msg2)
        self.assertNotEqual(rx_constructed_msg2, msg)

    def test_data_modulation(self):
        msg = "hello world!"
        msg2 = "abc"

        mod1 = self.scheme.modulateData(msg)
        mod2 = self.scheme.modulateData(msg)
        mod3 = self.scheme.modulateData(msg2)

        self.assertTrue(np.array_equal(mod1, mod2))
        self.assertFalse(np.array_equal(mod1, mod3))
        self.assertFalse(np.array_equal(mod2, mod3))

    def test_data_modulation_demodulation(self):
        msg = "hello world!"
        msg2 = "abcd"
        packet = XIPacket(buffer=msg)
        packet2 = XIPacket(buffer=msg2)

        mod1 = self.scheme.modulateData(packet.rep)
        mod2 = self.scheme.modulateData(packet.rep)
        mod3 = self.scheme.modulateData(packet2.rep)

        demod1 = self.scheme.demodulateData(mod1)
        demod2 = self.scheme.demodulateData(mod2)
        demod3 = self.scheme.demodulateData(mod3)

        demodPacket1 = XIPacket.createXIPacket(buffer=demod1)
        demodPacket2 = XIPacket.createXIPacket(buffer=demod2)
        demodPacket3 = XIPacket.createXIPacket(buffer=demod3)

        demod1Msg = demodPacket1.payload
        demod2Msg = demodPacket2.payload
        demod3Msg = demodPacket3.payload

        self.assertEqual(msg, demod1Msg)
        self.assertEqual(msg, demod2Msg)
        self.assertEqual(msg2, demod3Msg)


class TestBPSK(TestQPSK):
    scheme = ModulationFactory.chooseScheme('bpsk')


class Test4QAM(TestQPSK):

    scheme = ModulationFactory.chooseScheme(ModulationFactory.QAM4)

    def test_vectorized_demap(self):
        msg = "".join([chr(ord('a') + (x % 26)) for x in range(1000)])
        packet = XIPacket(buffer=msg)

        symbols = self.scheme.symbolMap(packet.rep)

        list_bytes = self.scheme.symbolVectorizedDemap(symbols)
        ret_msg = "".join([chr(x) for x in list_bytes])
        ret_packet = XIPacket.createXIPacket(buffer=ret_msg)

        self.assertEqual(msg, ret_packet.payload)

    def test_create_read_symbol_vectorized(self):
        msg = 'abc'
        msg2 = 'hello world'

        tx_buf = self.scheme.symbolMap(msg)
        tx_buf2 = self.scheme.symbolMap(msg2)

        rx_rec_msg = self.scheme.symbolVectorizedDemap(tx_buf)
        rx_rec_msg2 = self.scheme.symbolVectorizedDemap(tx_buf2)

        self.assertIsNotNone(rx_rec_msg)
        self.assertIsNotNone(rx_rec_msg2)

        rx_constructed_msg = "".join([chr(x) for x in rx_rec_msg])
        rx_constructed_msg2 = "".join([chr(x) for x in rx_rec_msg2])

        self.assertEqual(rx_constructed_msg, msg)
        self.assertEqual(rx_constructed_msg2, msg2)

        self.assertNotEqual(rx_constructed_msg, rx_constructed_msg2)
        self.assertNotEqual(rx_constructed_msg, msg2)
        self.assertNotEqual(rx_constructed_msg2, msg)


class Test16QAM(Test4QAM):

    scheme = ModulationFactory.chooseScheme(ModulationFactory.QAM16)


class TestSRRC(unittest.TestCase):
    def test(self):
        pass


if __name__ == '__main__':
    unittest.main()