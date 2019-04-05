import threading
from multiprocessing.pool import ThreadPool, Pool
import numpy as np
from timeit import default_timer as timer
import time
import logging
from pluto.pluto_sdr import PlutoSdr
# from ..networking.xi import XIPacket, XIPacketHeader, PACKET_TYPE

_msg = ""
_msg_once = None
_raw_msg = None
_msg_sent = False

_ioManager = None
_io_alive = False

_nonEmptyReceived = 0
_totalReceived = 0
_processingTime = 0
_readTime = 0
_rxUptime = 0

_received_msgs = []


def getIOManager(sdr, scheme):
    """
    Returns a singleton instance of PlutoIOManager
    as only one Pluto device will be managed by the
    application.
    """
    global _ioManager
    if _ioManager == None:
        _ioManager = _PlutoIOManager(sdr, scheme)

    else:
        _ioManager.set_scheme(scheme)

    return _ioManager


class _PlutoIOManager():
    def __init__(self, sdr, scheme):
        self._sdr = sdr
        self._scheme = scheme

    def _startPool(self, count, func, _type):
        if _type == 'thread':
            pool = ThreadPool(count)
        else:
            pool = Pool(count)
        threadArgs = {
            "stop": False,
            "pool": pool,
            "sdr": self._sdr,
            "scheme": self._scheme,
            "rxSamples": 2**18
        }
        thread = threading.Thread(target=func, args=[threadArgs])
        thread.start()
        return (thread, threadArgs, pool)

    def _startRxPool(self, count=2, _type=None):
        return self._startPool(count, _rxThreadFunc, _type)

    def _startTxPool(self, count=2, _type=None):
        return self._startPool(count, _txThreadFunc, _type)

    def set_scheme(self, scheme):
        self._scheme = scheme
        self._txThreadArgs['scheme'] = self._scheme
        self._rxThreadArgs['scheme'] = self._scheme

    def setRXProcessingFunc(self, func):
        self._rxThreadArgs['finalProcessingFunc'] = func

    def setRXSamples(self, rxSamples):
        if rxSamples > 0:
            self._rxThreadArgs['rxSamples'] = int(rxSamples)

    def getRXSamples(self):
        return self._rxThreadArgs['rxSamples']

    def startIO(self, readCount=2, writeCount=2, _type=None):
        global _io_alive, _msg_sent
        resetTotalPackets()
        resetValidPackets()
        resetProcessingTime()
        resetReadTime()
        resetRXUptime()
        _io_alive = True
        _msg_sent = False
        (txThread, txThreadArgs, txPool) = self._startTxPool(writeCount, _type)
        self._txThread = txThread
        self._txThreadArgs = txThreadArgs
        self._txPool = txPool

        (rxThread, rxThreadArgs, rxPool) = self._startRxPool(readCount, _type)
        self._rxThread = rxThread
        self._rxThreadArgs = rxThreadArgs
        self._rxPool = rxPool

    def stopIO(self):
        global _io_alive, _msg_sent, _msg, _msg_once
        # allows the threads to exit successfully
        _io_alive = False
        _msg_sent = False
        _msg = ""
        _msg_once = None
        # stop Output processes and threads
        self._txThreadArgs['stop'] = True
        self._txPool.close()

        # stop Input processes and threads
        self._rxThreadArgs['stop'] = True
        self._rxPool.close()

        # wait for threads to stop
        self._txThread.join()
        self._rxThread.join()

    def turnOffTx(self):
        global _msg_sent
        self._sdr.writeTx([])  # turns off TX
        _msg_sent = True

    def _set_msg(self, msg):
        global _msg, _msg_sent, _raw_msg
        if _msg != msg:
            _msg_sent = False
            _msg = msg
            _raw_msg = None

    def _set_msg_once(self, msg):
        global _msg_once, _msg_sent
        _msg_sent = False
        _msg_once = msg

    def _set_raw(self, txData):
        global _raw_msg, _msg_sent, _msg
        _msg_sent = False
        _msg = ""
        _raw_msg = txData

    def write(self, msg):
        self._set_msg(msg)

    def writeOnce(self, msg):
        self._set_msg_once(msg)

    def writeRaw(self, txData):
        self._set_raw(txData)

    def preprocess_msgs(self, msgs):
        fc = self._sdr.rx_lo_freq
        fs = self._sdr.sampling_frequency
        workerArgs = [[fc, fs, self._scheme, msg] for msg in msgs]
        res = self._txPool.map(_modulateTXData_unpack, workerArgs)
        return res


# the following functions will be used for I/O for the Pluto
def _readComplexRX(sdr, rxSamples):
    """
    Read Imaginary and Complex RX data
    """
    global _readTime

    readStart = timer()
    rxData = sdr.readRx(rxSamples, False)  # Imaginary & Real
    readEnd = timer()

    _readTime += readEnd - readStart
    return rxData


def _demodRXData(fc, fs, scheme, rxData):
    demod = timer()
    lengthUpsampledPilot = len(scheme._pilot_upsample)
    demodData = scheme.demodulateBetweenIndices(fc, fs, lengthUpsampledPilot,
                                                len(rxData), rxData)
    demodEnd = timer()
    logging.debug("Demod time: %fms" % ((demodEnd - demod) * 1e3))
    return demodData if demodData else ""


def _demodRXData_unpack(args):
    return _demodRXData(*args)


def getSamplesToCollect(args):
    rxSamples = 2**18
    if "rxSamples" in args:
        rxSamples = args["rxSamples"]
    return rxSamples


def _rxThreadFunc(args):
    rxPool = args["pool"]
    sdr = args["sdr"]
    scheme = args["scheme"]
    lastCollectTime = 0
    while not args["stop"] and _io_alive:
        rxSamplesToCollect = getSamplesToCollect(args)
        start = timer()

        waitForNewSamples(sdr, rxSamplesToCollect, lastCollectTime)
        rxData = _readComplexRX(sdr, rxSamplesToCollect)
        lastCollectTime = timer()

        processingStart = timer()
        nonEmptyMessages = processRXData(rxData, scheme, sdr, rxPool)
        processingEnd = timer()
        processingTime = processingEnd - processingStart

        logging.debug("Processed Messages: %d" % (len(nonEmptyMessages)))
        logging.debug("Processing Time: %fms" % (processingTime * 1e3))

        updateProcessingStats(processingTime)

        if _io_alive and 'finalProcessingFunc' in args:
            if args['finalProcessingFunc'] is not None:
                args['finalProcessingFunc'](nonEmptyMessages, rxData)

        end = timer()
        incrementRXUptime(end - start)


def waitForNewSamples(sdr, rxSamplesToCollect, lastCollectTime):
    """
    Waits for new samples if time to obtain a new set of 
    samples has not elapsed, otherwises does not wait.
    """
    timeForNewSamples = rxSamplesToCollect / sdr.sampling_frequency / 1e6
    timeSinceLastCollection = timer() - lastCollectTime
    if timeSinceLastCollection < timeForNewSamples:
        time.sleep(timeForNewSamples - timeSinceLastCollection)


def processRXData(rxData, scheme, sdr, rxPool):
    unfilter = timer()
    unfilteredData = unfilterData(scheme, rxData)
    startEndPairs = createStartEndPairs(scheme, unfilteredData)
    unfilterEnd = timer()

    worker = timer()
    results = _sendToWorker(rxPool, sdr, scheme, unfilteredData, startEndPairs)
    workerEnd = timer()

    nonEmptyMessages = filter(lambda x: len(x) > 0, results)
    nonEmpty = len(nonEmptyMessages)
    possible = len(startEndPairs)
    updateReceiverStats(nonEmpty, possible)

    logging.debug(
        "Unfilter + Find peaks time: %fms" % ((unfilterEnd - unfilter) * 1e3))
    logging.debug(
        "Result collection time: %fms" % ((workerEnd - worker) * 1e3))
    logging.debug("Number of results: %d" % len(results))
    # logging.debug("".join(results))

    return nonEmptyMessages


def unfilterData(scheme, rxData):
    unfilteredData = scheme.unfilterData(rxData)

    return unfilteredData


def createStartEndPairs(scheme, unfilteredData):
    startTimes, endTimes = scheme.findAllStartEnd(unfilteredData)

    # create all (start, end) pairs
    minLength = min(len(startTimes), len(endTimes))
    startEndPairs = [(startTimes[i], endTimes[i]) for i in range(minLength)]
    # TODO: figure out how to handle start with a missing end
    #       Ideas:
    #           - Create a buffer called remaining and prepend
    #             it to next unfiltered rxData set

    return startEndPairs


def _sendToWorker(rxPool, sdr, scheme, unfilteredData, startEndPairs):
    fc = sdr.rx_lo_freq
    fs = sdr.sampling_frequency
    lengthUpsampledPilot = len(scheme._pilot_upsample)
    workerArgs = [[
        fc, fs, scheme,
        unfilteredData[pair[0] - lengthUpsampledPilot:pair[1] + 1]
    ] for pair in startEndPairs]


    results = rxPool.map(_demodRXData_unpack, workerArgs) \
        if _io_alive else [""]

    return results


def updateReceiverStats(nonEmpty, totalPossible):
    global _totalReceived, _nonEmptyReceived
    # only update packet stats if io is still alive
    if _io_alive:
        _nonEmptyReceived += nonEmpty
        _totalReceived += totalPossible


def updateProcessingStats(processingTime):
    global _processingTime
    _processingTime += processingTime


def _modulateTXData(fc, fs, scheme, msg):
    return scheme.modulateData(fc, fs, msg)


def _modulateTXData_unpack(args):
    return _modulateTXData(*args)


def _writeMsg(sdr, scheme, msg):
    """
    Write data to TX
    """
    global _msg_sent
    fc = sdr.tx_lo_freq
    fs = sdr.sampling_frequency
    txData = _modulateTXData(fc, fs, scheme, msg)
    sdr.writeTx(txData)
    _msg_sent = True


def _txThreadFunc(args):
    global _msg_sent, _msg_once
    sdr = args["sdr"]
    scheme = args["scheme"]
    while not args["stop"]:
        if not _msg_sent:
            if _msg_once is not None:
                _writeMsg(sdr, scheme, _msg_once)
                _msg_once = None
            elif _msg != "":
                _writeMsg(sdr, scheme, _msg)
            elif _raw_msg is not None:
                sdr.writeTx(_raw_msg)
                _msg_sent = True


def getNonEmptyRatio():
    nonEmpty = float(getNonEmptyCount())
    total = getTotalCount() if getTotalCount() != 0 else 1
    return nonEmpty / total


def getNonEmptyCount():
    return _nonEmptyReceived


def getTotalCount():
    return _totalReceived


def getProcessingTime():
    return _processingTime


def getReadTime():
    return _readTime


def getRXUptime():
    return _rxUptime


def resetValidPackets():
    global _nonEmptyReceived
    _nonEmptyReceived = 0


def resetTotalPackets():
    global _totalReceived
    _totalReceived = 0


def resetProcessingTime():
    global _processingTime
    _processingTime = 0


def resetReadTime():
    global _readTime
    _readTime = 0


def resetRXUptime():
    global _rxUptime
    _rxUptime = 0


def incrementRXUptime(uptime):
    global _rxUptime
    _rxUptime += uptime