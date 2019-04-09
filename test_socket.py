from timeit import default_timer as timer
import time
import logging
import gui.analysis.throughputAnalysis as throughputAnalysis


def generateAZLetters(payloadSize):
    # generate letters a-z until payload size
    return "".join([chr(ord('a') + (x % 26)) for x in range(payloadSize)])


def generateAllOnes(payloadSize):
    return "".join(['1' for _ in range(payloadSize)])


def iterationStats(socket, msg, start, end, i):
    runtime = end - start
    throughput = throughputAnalysis.calculateThroughput(
        socket, msg, end - start)
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

    theoreticalThroughput = throughputAnalysis.calculateTheoreticalThroughput(
        socket, msg)
    runtime = end - start
    throughput = throughputAnalysis.calculateThroughput(socket, msg, runtime)
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
        throughput = throughputAnalysis.calculateThroughput(
            socket, msg, runtime)
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
    avgProcessing = throughputAnalysis.calculatePerPacketTime(socket)

    # calculate theoretical throughput
    theoreticalThroughput = throughputAnalysis.calculateTheoreticalThroughput(
        socket, msg) * 1e3 / 8  # in B/s
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
    socket.sendMsg(msg)
    socket.ioManager.setRXSamples(2**18)
    # no need for acknowledgements
    socket.sendAcks(False)

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

    finalResults(socket, msg, start, end)
    # showReadTimeStats(socket, msg, start, end)
    # showProcessingTimeStats(socket, msg, start, end)
    validPackets = socket.getValidPackets()
    runtime = end - start
    throughput = (validPackets * len(msg)) / runtime / 2**10 * 8  # in kbps
    return throughput


def testPacketACKs(socket):
    socket.sendMsgs(['a','b','c','d','e','f', 'g', 'h'])

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

    time.sleep(10)

    print(len(socket.getMsgs()))
    print(socket.getMsgs())


if __name__ == "__main__":
    from gui.plutoDevice.SimPlutoSdr import SimPlutoSdr
    from gui.plutoDevice.PlutoSdrWrapper import PlutoSdrWrapper
    from gui.modulation.Modulation import ModulationFactory
    from gui.networking.xi import XIPacket
    from gui.networking.socket import Socket

    logging.basicConfig(level=logging.INFO)

    scheme = ModulationFactory.chooseScheme(ModulationFactory.QAM)

    # sdr = SimPlutoSdr(P=scheme.P, alpha=scheme.alpha, desiredBandwidth=1.0)
    sdr = PlutoSdrWrapper()

    socket = Socket(sdr, scheme, ioReaders=1)

    payloadSize = 1023
    # payloadSize = XIPacket.maxPayload()

    msg = generateAZLetters(payloadSize)
    # msg = generateAllOnes(payloadSize)
    # throughput = modulationAnalysis(socket, msg)

    testPacketACKs(socket)

    socket.close()
    # print("Throughput: %f Kbps" % (throughput))

    print("done")