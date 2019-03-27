import unittest
from timeit import default_timer as timer
from Modulation import *
from ..networking.xi import XIPacket
import filter as f


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
        fc = 2250
        fs = 3
        scheme = ModulationFactory.chooseScheme('qam')
        settings = ModulationSettings(scheme)
        scheme2 = ModulationSettings.createModulation(settings.getString())

        schemeMod = scheme.modulateData(fc, fs, msg)
        scheme2Mod = scheme2.modulateData(fc, fs, msg)
        self.assertTrue(np.array_equal(schemeMod, scheme2Mod))

        schemeDemod = scheme.demodulateData(fc, fs, schemeMod)
        scheme2Demod = scheme2.demodulateData(fc, fs, schemeMod)
        self.assertEqual(schemeDemod, scheme2Demod)

        schemeDemod = scheme.demodulateData(fc, fs, scheme2Mod)
        scheme2Demod = scheme2.demodulateData(fc, fs, scheme2Mod)
        self.assertEqual(schemeDemod, scheme2Demod)


class TestModulationFactory(unittest.TestCase):
    def test_init(self):
        self.assertIsNotNone(ModulationFactory)


class TestModulation(unittest.TestCase):
    def test_init(self):
        self.assertIsNotNone(Modulation())


class TestBPSK(unittest.TestCase):
    def test_init(self):
        self.assertIsNotNone(ModulationFactory.chooseScheme('bpsk'))
        self.assertIsNotNone(
            ModulationFactory.chooseScheme(ModulationFactory.BPSK))

    def test_create_symbol(self):
        scheme = ModulationFactory.chooseScheme('bpsk')
        msg = 'abc'
        msg2 = 'hello world'

        self.assertIsNotNone(scheme.symbolMap(msg))
        self.assertIsNotNone(scheme.symbolMap(msg2))

        # tests that the buffer is the exact same when given two identical messages
        tx_buf = scheme.symbolMap(msg)
        tx_buf2 = scheme.symbolMap(msg)
        self.assertTrue(np.array_equal(tx_buf, tx_buf2))

        tx_buf = scheme.symbolMap(msg2)
        tx_buf2 = scheme.symbolMap(msg2)
        self.assertTrue(np.array_equal(tx_buf, tx_buf2))

        # test that the buffers are not the exact same when given two different messages
        tx_buf = scheme.symbolMap(msg)
        tx_buf2 = scheme.symbolMap(msg2)
        self.assertFalse(np.array_equal(tx_buf, tx_buf2))

        tx_buf = scheme.symbolMap(msg2)
        tx_buf2 = scheme.symbolMap(msg)
        self.assertFalse(np.array_equal(tx_buf, tx_buf2))

    def test_create_read_symbol(self):
        pass


class TestQPSK(unittest.TestCase):
    def test_init(self):
        self.assertIsNotNone(ModulationFactory.chooseScheme('qpsk'))
        self.assertIsNotNone(ModulationFactory.chooseScheme('qam'))
        self.assertIsNotNone(
            ModulationFactory.chooseScheme(ModulationFactory.QPSK))
        self.assertIsNotNone(
            ModulationFactory.chooseScheme(ModulationFactory.QAM))

    def test_create_symbol(self):
        scheme = ModulationFactory.chooseScheme('qpsk')
        msg = 'abc'
        msg2 = 'hello world'

        self.assertIsNotNone(scheme.symbolMap(msg))
        self.assertIsNotNone(scheme.symbolMap(msg2))

        # tests that the buffer is the exact same when given two identical messages
        tx_buf = scheme.symbolMap(msg)
        tx_buf2 = scheme.symbolMap(msg)
        self.assertTrue(np.array_equal(tx_buf, tx_buf2))

        tx_buf = scheme.symbolMap(msg2)
        tx_buf2 = scheme.symbolMap(msg2)
        self.assertTrue(np.array_equal(tx_buf, tx_buf2))

        # test that the buffers are not the exact same when given two different messages
        tx_buf = scheme.symbolMap(msg)
        tx_buf2 = scheme.symbolMap(msg2)
        self.assertFalse(np.array_equal(tx_buf, tx_buf2))

        tx_buf = scheme.symbolMap(msg2)
        tx_buf2 = scheme.symbolMap(msg)
        self.assertFalse(np.array_equal(tx_buf, tx_buf2))

    def test_timing(self):
        scheme = ModulationFactory.chooseScheme('qpsk')
        largeMsg = [chr(ord('a') + (x % 26)) for x in range(int(2**10))]
        largerMsg = [chr(ord('a') + (x % 26)) for x in range(int(2**12))]

        fc = 2.2e9
        fs = 3e6

        start = timer()
        tx_buf = scheme.modulateData(fc, fs, largeMsg)
        end = timer()
        print("Large tx buffer creation time: %fus" % ((end - start) * 1e6))

        start = timer()
        tx_buf2 = scheme.modulateData(fc, fs, largerMsg)
        end = timer()
        print(
            "Very large tx buffer creation time: %fus" % ((end - start) * 1e6))

        start = timer()
        rx_rec_msg = scheme.demodulateData(fc, fs, tx_buf)
        end = timer()
        print("Large rx buffer read time: %fus" % ((end - start) * 1e6))

        start = timer()
        rx_rec_msg2 = scheme.demodulateData(fc, fs, tx_buf2)
        end = timer()
        print("Very large rx buffer read time: %fus" % ((end - start) * 1e6))

    def test_create_read_symbol(self):
        scheme = ModulationFactory.chooseScheme('qpsk')
        msg = 'abc'
        msg2 = 'hello world'

        tx_buf = scheme.symbolMap(msg)
        tx_buf2 = scheme.symbolMap(msg2)

        rx_rec_msg = scheme.symbolDemap(tx_buf)
        rx_rec_msg2 = scheme.symbolDemap(tx_buf2)

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
        scheme = ModulationFactory.chooseScheme('qpsk')
        msg = "hello world!"
        msg2 = "abc"
        fc = 12000
        fs = 44100

        mod1 = scheme.modulateData(fc, fs, msg)
        mod2 = scheme.modulateData(fc, fs, msg)
        mod3 = scheme.modulateData(fc, fs, msg2)

        self.assertTrue(np.array_equal(mod1, mod2))
        self.assertFalse(np.array_equal(mod1, mod3))
        self.assertFalse(np.array_equal(mod2, mod3))

    def test_data_modulation_demodulation(self):
        scheme = ModulationFactory.chooseScheme('qpsk')
        msg = "hello world!"
        msg2 = "abcd"
        packet = XIPacket(buffer=msg)
        packet2 = XIPacket(buffer=msg2)
        fc = 12000
        fs = 44100

        mod1 = scheme.modulateData(fc, fs, packet.rep)
        mod2 = scheme.modulateData(fc, fs, packet.rep)
        mod3 = scheme.modulateData(fc, fs, packet2.rep)

        demod1 = scheme.demodulateData(fc, fs, mod1)
        demod2 = scheme.demodulateData(fc, fs, mod2)
        demod3 = scheme.demodulateData(fc, fs, mod3)

        demodPacket1 = XIPacket.createXIPacket(buffer=demod1)
        demodPacket2 = XIPacket.createXIPacket(buffer=demod2)
        demodPacket3 = XIPacket.createXIPacket(buffer=demod3)

        demod1Msg = demodPacket1.payload
        demod2Msg = demodPacket2.payload
        demod3Msg = demodPacket3.payload

        self.assertEqual(msg, demod1Msg)
        self.assertEqual(msg, demod2Msg)
        self.assertEqual(msg2, demod3Msg)


class TestSRRC(unittest.TestCase):
    def test(self):
        pass


if __name__ == '__main__':
    unittest.main()