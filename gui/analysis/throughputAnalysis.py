from timeit import default_timer as timer
import time
import logging
from ..networking.xi import XIPacket


def calculateThroughput(socket, msg, runtime):
    """
    Calculates Throughput in Kbps
    """
    packet = XIPacket(buffer=msg)
    return (
        socket.getValidPackets() * packet.length) / runtime / 2**10 * 8  # in kbps


def calculateTheoreticalThroughput(socket, msg):
    """
    Calculates Theoretical Throughput in Kbps
    including packet overhead
    """
    fs = socket.sdr.sampling_frequency
    txDataSize = socket.scheme.modulateData(msg)
    packet = XIPacket(buffer=msg)
    theoreticalThroughput = fs * 1e6 / len(
        txDataSize) * packet.length / 2**10 * 8  # in kbps
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