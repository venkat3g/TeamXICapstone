import Throughput as page
import Throughput_support as support
import PlutoController
import ThreadWrapper
import time
from timeit import default_timer as timer
from analysis import throughputAnalysis
from networking.socket import Socket

msgSize = 26
currentMsg = ""
threadUpdateTime = 1
updateGUIThread = None
socket = None
startTime = None


def generateAZLetters(payloadSize):
    # generate letters a-z until payload size
    return "".join([chr(ord('a') + (x % 26)) for x in range(payloadSize)])


def setGUIUpdateTime(timeStr):
    global threadUpdateTime
    if len(timeStr) > 0:
        threadUpdateTime = int(timeStr)


def setMsgSize(sizeStr):
    global msgSize
    if len(sizeStr) > 0:
        msgSize = int(sizeStr)


def init_throughput_gui():
    support.msgSize_value.set(str(msgSize))
    support.guiUpdate_value.set(str(threadUpdateTime))
    support.startingRXSample_value.set(str(2**18))
    support.dynamicAdjust.set('0')


def set_bindings():
    support.msgSize_value.trace(
        'w', lambda *args: setMsgSize(support.msgSize_value.get()))
    support.guiUpdate_value.trace(
        'w', lambda *args: setGUIUpdateTime(support.guiUpdate_value.get()))


def updateGUI():
    throughputUnit = 'Kbps'
    throughput = throughputAnalysis.calculateThroughput(
        socket, currentMsg,
        timer() - startTime)

    tThroughput = throughputAnalysis.calculateTheoreticalThroughput(
        socket, currentMsg)
    processingTime = socket.getProcessingTime()
    processingTimeUnit = 's'

    perPacketUnit = 'ms'
    perPacketTime = throughputAnalysis.calculatePerPacketTime(socket)
    tPerPacketTime = throughputAnalysis.calculateTPerPacketTime(
        socket, currentMsg)

    support.vpr_value.set(str(socket.getValidPacketRatio() * 100) + '%')
    support.validPackets_value.set(str(socket.getValidPackets()))
    support.totalPackets_value.set(str(socket.getTotalPackets()))

    support.throughput_value.set(str(throughput) + throughputUnit)
    support.perPacket_value.set(str(perPacketTime * 1e3) + perPacketUnit)
    support.processingTime_value.set(str(processingTime) + processingTimeUnit)

    support.tThroughput_value.set(str(tThroughput) + throughputUnit)
    support.tPerPacket_value.set(str(tPerPacketTime * 1e3) + perPacketUnit)

    support.adjustedRXSamples_value.set(socket.ioManager.getRXSamples())


def updateThread(args):
    global startTime
    startTime = timer()
    while not args['done']:
        if socket is not None:
            updateGUI()
            if support.dynamicAdjust.get() == '1':
                # dynamically adjust samples if selected in GUI
                socket.adjustRXSamples()
        time.sleep(threadUpdateTime)


def startAnalysis():
    global updateGUIThread, socket, currentMsg

    currentMsg = generateAZLetters(msgSize)
    socket = Socket(PlutoController.getSdr(), PlutoController.getScheme())
    socket.ioManager.setRXSamples(int(support.startingRXSample_value.get()))
    socket.sendMsg(currentMsg)

    updateGUIThread = ThreadWrapper.ThreadController(updateThread)

    # allow process pools for the underlying
    # socket ioManager to "warm up"
    time.sleep(2)

    # Reset values to for analysis of modulation scheme
    # reset packet counts for throughput measurement
    socket.resetTotalPackets()
    socket.resetValidPackets()
    # reset processsing time and read time for analysis
    socket.resetProcessingTime()
    socket.resetReadTime()
    socket.resetRXUptime()

    updateGUIThread.start()


def stopAnalysis():
    global updateGUIThread, socket

    if updateGUIThread is not None:
        updateGUIThread.stop()
        updateGUIThread = None

    if socket is not None:
        socket.close()
        del socket
        socket = None


def start(root, onExit):
    (w, top) = page.create_Throughput_TL(root)

    init_throughput_gui()
    set_bindings()

    top.StartButton.bind('<ButtonRelease-1>', lambda *args: startAnalysis())
    top.StopButton.bind('<ButtonRelease-1>', lambda *args: stopAnalysis())

    def close():
        global updateGUIThread, socket
        if updateGUIThread is not None:
            updateGUIThread.stop()
            updateGUIThread = None
        if socket is not None:
            socket.close()
            socket = None

        page.destroy_Throughput_TL()
        onExit()

    w.protocol("WM_DELETE_WINDOW", close)