from ..plutoDevice import plutoIO
from xi import XIPacket, XIPacketHeader, PACKET_TYPE
from ..ThreadWrapper import ThreadController
import threading
import numpy as np


class Socket:
    def __init__(self, sdr, scheme, ioReaders=1, ioWriters=1):
        self.sdr = sdr
        self.scheme = scheme
        self.ioReaders = ioReaders
        self.ioWriters = ioWriters

        self.ioManager = plutoIO.getIOManager(sdr, scheme)
        self.ioManager.startIO(self.ioReaders, self.ioWriters)
        self.ioManager.setRXProcessingFunc(self.processPackets)

        self.msgsThreadController = ThreadController(socket_send_msgs)
        self.msgsThreadController.collectionThreadArgs['self'] = self
        self.msgsThreadController.collectionThreadArgs['msgs'] = []
        self.msgsThreadController.start()

        self.sendMessageSemaphore = threading.Semaphore(
            2**XIPacketHeader()._seq_num_bit_length)

        self._received_msgs = set()
        self._recent_tx_msg = ''
        self._recent_rx_msg = ''
        self._recent_rx = np.array([])
        self._validPackets = 0
        self._totalPackets = 0

        self._sendAcks = True

    def sendAcks(self, sendAcks):
        self._sendAcks = sendAcks

    def close(self):
        maxSeqNumber = 2**XIPacketHeader()._seq_num_bit_length
        for _ in range(maxSeqNumber):
            self.sendMessageSemaphore.release()

        self.msgsThreadController.stop()
        self.ioManager.stopIO()

    def sendMsg(self, msg):
        packet = XIPacket(buffer=msg, type=PACKET_TYPE.DATA, seqNum=0)
        self.ioManager.write(packet.rep)
        self._recent_tx_msg = packet.rep

    def stopTransmission(self):
        self.ioManager.turnOffTx()

    def getRecentMsg(self):
        return self._recent_rx_msg

    def getRecentRx(self):
        return self._recent_rx

    def getRecentTx(self):
        txData = self.scheme.modulateData(self.sdr.tx_lo_freq,
                                          self.sdr.sampling_frequency,
                                          self._recent_tx_msg)
        return txData

    def sendMsgs(self, msgs):
        self.msgsThreadController.collectionThreadArgs['msgs'].extend(msgs)

    def getMsgs(self):
        return [packet.payload for packet in self._received_msgs]

    def getValidPacketRatio(self):
        valid = float(self._validPackets)
        total = self._totalPackets if self._totalPackets != 0 else 1
        return valid / total

    def getValidPackets(self):
        return self._validPackets

    def getTotalPackets(self):
        return self._totalPackets

    def resetValidPackets(self):
        self._validPackets = 0

    def resetTotalPackets(self):
        self._totalPackets = 0

    # access PlutoIO operations directly from socket object
    def getProcessingTime(self):
        return plutoIO.getProcessingTime()

    def getReadTime(self):
        return plutoIO.getReadTime()

    def getRXUptime(self):
        return plutoIO.getRXUptime()

    def resetProcessingTime(self):
        return plutoIO.resetProcessingTime()

    def resetReadTime(self):
        return plutoIO.resetReadTime()

    def resetRXUptime(self):
        return plutoIO.resetRXUptime()

    def processPackets(self, packetReps, rxData):
        self._recent_rx = rxData

        packets = [XIPacket.createXIPacket(x) for x in packetReps]
        self._totalPackets += len(packets)

        packets = filter(lambda x: x is not None,
                         packets)  # get rid of all invalid packets
        self._validPackets += len(packets)

        packets = list(set(packets))  # get rid of duplicates

        if len(packets) > 0:
            self.processPacketReps(packets)
            if self._sendAcks:
                self.findACK(packets)
            self._recent_rx_msg = packets[len(packets) - 1].payload
            packets.sort(key=lambda x: x.header.seqNum)
            for packet in packets:
                self._received_msgs.add(packet)
        else:
            self._recent_rx_msg = ""

        self.adjustRXSamples()

    def adjustRXSamples(self):
        """
        Dynamically adjusts RX samples to attempt to increase throughput.
        """
        currentRXSamples = self.ioManager.getRXSamples()
        if self.getValidPacketRatio() < 0.9:
            # increase RX samples to see if our percentage goes up.
            # increase by 10%
            self.ioManager.setRXSamples(currentRXSamples * 1.1)
        elif self.getValidPacketRatio() > 0.95:
            # decrease RX samples to see if our percentage goes down.
            # decrease by 5%
            if currentRXSamples * 0.95 > 1024:
                # prevent rxSamples from going to low, really only an issues for Sim
                self.ioManager.setRXSamples(currentRXSamples * 0.95)

    def processPacketReps(self, packets):
        packets.sort(key=lambda x: x.header.seqNum)

        # sends acks in order since we care about
        # the order of packets received
        lastSeqNumber = packets[0].header.seqNum
        for packet in packets:
            if packet.header.type == PACKET_TYPE.DATA:
                # only update sequence number if sequence number
                # is one plus the previous sequence number
                if lastSeqNumber + 1 == packet.header.seqNum:
                    lastSeqNumber = packet.header.seqNum

        # send an ack up until the most recent sequence number in order
        # acking that we have received until sequence number correctly
        if self._sendAcks:
            self.sendACK(lastSeqNumber)

    def findACK(self, packets):
        packets = filter(lambda x: x.header.type == PACKET_TYPE.ACK, packets)
        if len(packets) > 0:
            packets.sort(key=lambda x: x.header.seqNum, reverse=True)

            lastSeqNumber = packets[0].header.seqNum

            # if we received this ack this means the
            # client received all of the message until
            # the seq num successfully.
            for _ in range(lastSeqNumber):
                # release a value from the semaphore for
                # each sequence number acked
                self.sendMessageSemaphore.release()

    def sendACK(self, seqNum):
        # directly send ack on the tx line
        # this ignores the message queue
        ackPacket = XIPacket(type=PACKET_TYPE.ACK, seqNum=seqNum)
        self.ioManager.writeOnce(ackPacket.rep)


def socket_send_msgs(args):
    ref = args['self']
    maxSeqNumber = 2**XIPacketHeader()._seq_num_bit_length
    msgs = args['msgs']
    while not args['done']:
        while len(msgs) > 0:
            minLen = maxSeqNumber if maxSeqNumber < len(msgs) else len(msgs)
            packets = [
                XIPacket(
                    buffer=msg,
                    type=PACKET_TYPE.DATA,
                    seqNum=(i % maxSeqNumber))
                for i, msg in enumerate(msgs[:minLen])
            ]
            msgs_to_send = [packet.rep for packet in packets]
            preprocessed_msgs = ref.ioManager.preprocess_msgs(msgs_to_send)

            # remove messages from queue of messages to send
            for i in range(minLen):
                msgs.pop(0)

            # acquire send message semaphore for all message to be sent
            for i in range(0, maxSeqNumber):
                ref.sendMessageSemaphore.acquire()

            txData = np.concatenate(tuple(preprocessed_msgs))
            ref.ioManager.writeRaw(txData)