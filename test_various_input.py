from timeit import default_timer as timer
import time
import logging
import multiprocessing
import multiprocessing.pool


def generateAZLetters(payloadSize):
    # generate letters a-z until payload size
    return "".join([chr(ord('a') + (x % 26)) for x in range(payloadSize)])


def generateAllOnes(payloadSize):
    return "".join(['1' for _ in range(payloadSize)])


def iterationStats(socket, msg, start, end, i):
    runtime = end - start
    throughput = (
        socket.getValidPackets() * len(msg)) / runtime / 2**10 * 8  # in kbps
    print(" ")
    print("-------------------------------------------------------------")
    print("\t\tIteration %d Results" % (i + 1))
    print("-------------------------------------------------------------")
    print("Valid Packet Ratio (v/t)\n\t(where 0/0 -> 0.0): %f (%d/%d)" %
          (socket.getValidPacketRatio(), socket.getValidPackets(),
           socket.getTotalPackets()))
    print("RX Thread Uptime: %f seconds" % (socket.getRXUptime()))
    print("Receiver Throughput: %f Kbps" % (throughput))


def finalResults(socket, msg, start, end):

    print(" ")
    print("Payload Size: %d, RX Pool Size: %d" % (len(msg), socket.ioReaders))
    print("-------------------------------------------------------------")
    print("\t\tFinal Results")
    print("-------------------------------------------------------------")
    print("Valid Packet Ratio (v/t)\n\t(where 0/0 -> 0.0): %f (%d/%d)" %
          (socket.getValidPacketRatio(), socket.getValidPackets(),
           socket.getTotalPackets()))

    fs = socket.sdr.sampling_frequency
    txDataSize = socket.scheme.modulateData(msg)
    theoreticalThroughput = fs * 1e6 / len(txDataSize) * len(
        msg) / 2**10 * 8  # in kbps
    runtime = end - start
    throughput = (
        socket.getValidPackets() * len(msg)) / runtime / 2**10 * 8  # in kbps
    print("Runtime: %f seconds" % (runtime))
    print("RX Thread Uptime: %f seconds" % (socket.getRXUptime()))
    print("Theoretical Receiver Throughput: %f Kbps" % (theoreticalThroughput))
    print("Receiver Throughput: %f Kbps" % (throughput))
    print("Receiver Throughput: %f KB/s" % (throughput / 8))
    return throughput


def showReadTimeStats(socket, msg, start, end):
    readTime = socket.getReadTime()
    validPackets = socket.getValidPackets()
    avgRead = readTime / validPackets if validPackets != 0 else 1

    print(" ")
    print("-------------------------------------------------------------")
    print("\t\tRead Time Statistics")
    print("-------------------------------------------------------------")
    print("RX Read Time: %f seconds" % (readTime))
    print("Average Read Time per packet: %f ms" % (avgRead * 1e3))

    reductionPercentages = [10 * x for x in range(2, 10, 2)]

    for reduction in reductionPercentages:
        reducedReadTime = readTime * (reduction / 100.0)
        runtime = end - start - reducedReadTime
        throughput = (socket.getValidPackets() *
                      len(msg)) / runtime / 2**10 * 8  # in kbps
        validPackets = validPackets if validPackets != 0 else 1

        print(" ")
        print("Reduce Read Time by %d%%: %f seconds" % (reduction,
                                                        reducedReadTime))
        print("Reduce per packet time by %f ms" %
              (reducedReadTime / validPackets * 1e3))
        print("Reduced Throughput: %f Kbps" % (throughput))


def showProcessingTimeStats(socket, msg, start, end):
    processingTime = socket.getProcessingTime()
    validPackets = socket.getValidPackets()
    avgProcessing = processingTime / validPackets if validPackets != 0 else 1

    # calculate theoretical throughput
    fs = socket.sdr.sampling_frequency
    txDataSize = socket.scheme.modulateData(msg)
    theoreticalThroughput = fs * 1e6 / len(txDataSize) * len(msg)  # in B/s
    avgTheoreticalProcessing = len(msg) / theoreticalThroughput

    print(" ")
    print("-------------------------------------------------------------")
    print("\t\tProcessing Time Statistics")
    print("-------------------------------------------------------------")
    print("Processing Time: %f seconds" % (processingTime))
    print("Average Processing Time per packet (%d packets): %f ms" %
          (validPackets, avgProcessing * 1e3))
    print("Theoretical Average Processing Time per packet: %f ms" %
          (avgTheoreticalProcessing * 1e3))

    increasePercentages = [10 * x for x in range(2, 10, 2)]

    validPackets = validPackets if validPackets != 0 else 1
    for increase in increasePercentages:
        perPacketTime = avgTheoreticalProcessing * (1 + increase / 100.0)
        increasedPerPacket = perPacketTime - avgTheoreticalProcessing
        processingTime = perPacketTime * validPackets

        runtime = processingTime
        throughput = (validPackets * len(msg)) / runtime / 2**10 * 8  # in kbps

        print(" ")
        print("Theoretical Processing Time (for %d packets +%d%%): %f seconds"
              % (validPackets, increase, processingTime))
        print("Theoretical per packet time: %f ms (increased by %f ms)" %
              (perPacketTime * 1e3, increasedPerPacket * 1e3))
        print("Theoretical Throughput: %f Kbps" % (throughput))


def modulationAnalysis(socket, msg):
    # give some time for ioManager to "warm up" Process Pools
    time.sleep(2)

    # Reset values to for analysis of modulation scheme
    # reset packet counts for throughput measurement
    socket.resetTotalPackets()
    socket.resetValidPackets()
    # reset processsing time and read time for analysis
    socket.resetProcessingTime()
    socket.resetReadTime()
    socket.resetRXUptime()

    # measures data throughput over x iteration
    x = 1
    start = timer()
    for i in range(x):
        # each iteration is y seconds
        y = 5
        time.sleep(y)
        end = timer()
        # show statistics for this iteration
        # iterationStats(socket, msg, start, end, i)

    # finalResults(socket, msg, start, end)
    # showReadTimeStats(socket, msg, start, end)
    # showProcessingTimeStats(socket, msg, start, end)
    validPackets = socket.getValidPackets()
    runtime = end - start
    throughput = (validPackets * len(msg)) / runtime / 2**10 * 8  # in kbps
    return throughput


def testPacketACKs(socket):
    time.sleep(10)
    socket.close()

    print(len(socket.getMsgs()))
    print(socket.getMsgs())


def writeToCSVFile(results, filename):
    with open(filename, 'w') as resultsFile:
        import csv
        keys = results[0].keys()
        keys.remove('throughput')
        keys.append('throughput')
        dict_writer = csv.DictWriter(resultsFile, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

def getResults(rxSamples, msg):
    from gui.plutoDevice.SimPlutoSdr import SimPlutoSdr
    from gui.plutoDevice.PlutoSdrWrapper import PlutoSdrWrapper
    from gui.modulation.Modulation import ModulationFactory
    from gui.networking.xi import XIPacket
    from gui.networking.socket import Socket
    scheme = ModulationFactory.chooseScheme(ModulationFactory.QAM)
    sdr = SimPlutoSdr(P=scheme.P, alpha=scheme.alpha, desiredBandwidth=1.0)
    socket = Socket(sdr, scheme, ioReaders=1)
    socket.ioManager.setRXSamples(rxSamples)
    socket.sendMsg(msg)
    throughput = modulationAnalysis(socket, msg)
    result = {
        "msgSize": len(msg),
        "rxSamples": rxSamples,
        "throughput": throughput
    }
    socket.close()

    return result


def getResults_unpack(args):
    return getResults(*args)


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess

if __name__ == "__main__":
    from gui.plutoDevice.SimPlutoSdr import SimPlutoSdr
    from gui.plutoDevice.PlutoSdrWrapper import PlutoSdrWrapper
    from gui.modulation.Modulation import ModulationFactory
    from gui.networking.xi import XIPacket
    from gui.networking.socket import Socket
    from multiprocessing import Pool

    logging.basicConfig(level=logging.INFO)

    scheme = ModulationFactory.chooseScheme(ModulationFactory.QAM)

    sdr = SimPlutoSdr(P=scheme.P, alpha=scheme.alpha, desiredBandwidth=1.0)
    # sdr = PlutoSdrWrapper()

    socket = Socket(sdr, scheme, ioReaders=1)

    payloadSize = 2**7
    # payloadSize = XIPacket.maxPayload()

    msg = generateAZLetters(payloadSize)
    # msg = generateAllOnes(payloadSize)
    socket.sendMsg(msg)

    results = []
    msgs = [generateAZLetters(size) for size in range(500, 1024, 5)]
    params = []
    for rxSamples in [2**x for x in range(17, 19)]:
        for msg in msgs:
            params.append([rxSamples, msg])
    processPool = MyPool(4)

    start = timer()
    results = processPool.map(getResults_unpack, params)
    print("Parallel Processing Time: %f seconds" % (timer() - start))

    writeToCSVFile(results, 'multi6.csv')
    socket.close()
    print("done")
    # testPacketACKs(socket)