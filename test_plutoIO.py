from timeit import default_timer as timer
import time
import logging


def generateAZLetters(payloadSize):
    # generate letters a-z until payload size
    return "".join([chr(ord('a') + (x % 26)) for x in range(payloadSize)])


def generateAllOnes(payloadSize):
    return "".join(['1' for _ in range(payloadSize)])


def iterationStats(plutoIO, msg, start, end, i):
    runtime = end - start
    throughput = (
        plutoIO.getNonEmptyCount() * len(msg)) / runtime / 2**10 * 8  # in kbps
    print(" ")
    print("-------------------------------------------------------------")
    print("\t\tIteration %d Results" % (i + 1))
    print("-------------------------------------------------------------")
    print("Valid Packet Ratio (v/t)\n\t(where 0/0 -> 0.0): %f (%d/%d)" %
          (plutoIO.getNonEmptyRatio(), plutoIO.getNonEmptyCount(),
           plutoIO.getTotalCount()))
    print("RX Thread Uptime: %f seconds" % (plutoIO.getRXUptime()))
    print("Receiver Throughput: %f Kbps" % (throughput))


def finalResults(plutoIO, msg, start, end):
    print(" ")
    print("-------------------------------------------------------------")
    print("\t\tFinal Results")
    print("-------------------------------------------------------------")
    print("Valid Packet Ratio (v/t)\n\t(where 0/0 -> 0.0): %f (%d/%d)" %
          (plutoIO.getNonEmptyRatio(), plutoIO.getNonEmptyCount(),
           plutoIO.getTotalCount()))
    # print(len(plutoIO._received_msgs))
    # print([(len(m),m) for m in plutoIO._received_msgs])

    runtime = end - start
    throughput = (
        plutoIO.getNonEmptyCount() * len(msg)) / runtime / 2**10 * 8  # in kbps
    print("Runtime: %f seconds" % (runtime))
    print("RX Thread Uptime: %f seconds" % (plutoIO.getRXUptime()))
    print("Receiver Throughput: %f Kbps" % (throughput))
    print("Receiver Throughput: %f KB/s" % (throughput / 8))


def showReadTimeStats(plutoIO, msg, start, end):
    readTime = plutoIO.getReadTime()
    nonEmptyPackets = plutoIO.getNonEmptyCount()
    avgRead = readTime / nonEmptyPackets if nonEmptyPackets != 0 else 1

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
        throughput = (plutoIO.getNonEmptyCount() *
                      len(msg)) / runtime / 2**10 * 8  # in kbps
        nonEmptyPackets = nonEmptyPackets if nonEmptyPackets != 0 else 1

        print(" ")
        print("Reduce Read Time by %d%%: %f seconds" % (reduction,
                                                        reducedReadTime))
        print("Reduce per packet time by %f ms" %
              (reducedReadTime / nonEmptyPackets * 1e3))
        print("Reduced Throughput: %f Kbps" % (throughput))


def showProcessingTimeStats(plutoIO, msg, start, end):
    processingTime = plutoIO.getProcessingTime()
    nonEmpty = plutoIO.getNonEmptyCount()
    avgProcessing = processingTime / nonEmpty if nonEmpty != 0 else 1

    print(" ")
    print("-------------------------------------------------------------")
    print("\t\tProcessing Time Statistics")
    print("-------------------------------------------------------------")
    print("Processing Time: %f seconds" % (processingTime))
    print("Average Processing Time per packet: %f ms" % (avgProcessing * 1e3))

    reductionPercentages = [10 * x for x in range(2, 10, 2)]

    for reduction in reductionPercentages:
        reducedProcessingTime = processingTime * (reduction / 100.0)
        runtime = end - start - reducedProcessingTime
        throughput = (plutoIO.getNonEmptyCount() *
                      len(msg)) / runtime / 2**10 * 8  # in kbps
        nonEmpty = nonEmpty if nonEmpty != 0 else 1

        print(" ")
        print("Reduce Processing Time by %d%%: %f seconds" %
              (reduction, reducedProcessingTime))
        print("Reduce per packet time by %f ms" %
              (reducedProcessingTime / nonEmpty * 1e3))
        print("Reduced Throughput: %f Kbps" % (throughput))


def modulationAnalysis(ioManager, plutoIO, msg):
    # give some time for ioManager to "warm up" Process Pools
    time.sleep(2)

    # Reset values to for analysis of modulation scheme
    # reset packet counts for throughput measurement
    plutoIO.resetTotalPackets()
    plutoIO.resetValidPackets()
    # reset processsing time and read time for analysis
    plutoIO.resetProcessingTime()
    plutoIO.resetReadTime()
    plutoIO.resetRXUptime()

    # measures data throughput over x iteration
    x = 1
    start = timer()
    for i in range(x):
        # each iteration is y seconds
        y = 5
        time.sleep(y)
        end = timer()
        # show statistics for this iteration
        iterationStats(plutoIO, msg, start, end, i)

    ioManager.stopIO()

    finalResults(plutoIO, msg, start, end)
    showReadTimeStats(plutoIO, msg, start, end)
    showProcessingTimeStats(plutoIO, msg, start, end)


def testPacketACKs(ioManager, plutoIO):
    time.sleep(10)
    ioManager.stopIO()

    print(len(plutoIO._received_msgs))
    print(plutoIO._received_msgs)


if __name__ == "__main__":
    import gui.plutoDevice.plutoIO as plutoIO
    from gui.plutoDevice.SimPlutoSdr import SimPlutoSdr
    from gui.plutoDevice.PlutoSdrWrapper import PlutoSdrWrapper
    from gui.modulation.Modulation import ModulationFactory
    from gui.networking.xi import XIPacket

    logging.basicConfig(level=logging.INFO)

    getIOManager = plutoIO.getIOManager

    scheme = ModulationFactory.chooseScheme(ModulationFactory.QAM)

    # sdr = SimPlutoSdr(P=scheme.P, alpha=scheme.alpha, desiredBandwidth=1.0)
    sdr = PlutoSdrWrapper()

    ioManager = getIOManager(sdr, scheme)

    ioManager.startIO(1, 1)

    # ioManager.write("Hello World")

    payloadSize = 2**5
    payloadSize = XIPacket.maxPayload()

    msg = generateAZLetters(payloadSize)
    # msg = generateAllOnes(payloadSize)
    ioManager.write(msg)
    # TODO: Remove anything that isn't "write"
    # ioManager.writeMsgs(['a', 'b', 'c', 'd', 'e', 'f'])
    # ioManager.writeMsgs([chr(ord('a') + (x % 26)) for x in range(26)])

    # ioManager.writeFile(
    #     "C:/Users/Venkat/OneDrive/College(OSU)/Senior (2018-2019)/SP 19/ECE 4900/teamxicapstone/gui/messages/5KB.txt"
    # )
    # ioManager.writeFile("C:/Users/venka/OneDrive/College(OSU)/Senior (2018-2019)/SP 19/ECE 4900/teamxicapstone/gui/messages/1MB.txt")

    modulationAnalysis(ioManager, plutoIO, msg)
    # testPacketACKs(ioManager, plutoIO)
