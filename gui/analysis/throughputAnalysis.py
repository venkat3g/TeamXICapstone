from timeit import default_timer as timer
import time
import logging


def calculateThroughput(socket, msg, runtime):
    """
    Calculates Throughput in Kbps
    """
    return (
        socket.getValidPackets() * len(msg)) / runtime / 2**10 * 8  # in kbps


def calculateTheoreticalThroughput(socket, msg):
    """
    Calculates Theoretical Throughput in Kbps
    """
    fc = socket.sdr.tx_lo_freq
    fs = socket.sdr.sampling_frequency
    txDataSize = socket.scheme.modulateData(fc, fs, msg)
    theoreticalThroughput = fs * 1e6 / len(txDataSize) * len(
        msg) / 2**10 * 8  # in kbps
    return theoreticalThroughput


def calculatePerPacketTime(socket):
    """
    Calculates per Packet Time in seconds
    """
    processingTime = socket.getProcessingTime()
    validPackets = socket.getValidPackets()
    avgProcessing = processingTime / validPackets if validPackets != 0 else 1

    return avgProcessing


def calculateTPerPacketTime(socket, msg):
    """
    Calculates Theoretical per Packet Time in seconds
    """
    theoreticalThroughput = calculateTheoreticalThroughput(
        socket, msg) * 1e3 / 8  # in B/s
    avgTheoreticalProcessing = len(msg) / theoreticalThroughput

    return avgTheoreticalProcessing