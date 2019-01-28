import random
import testPlot
import time

def generateRandomNumber(max = 10, min = 1):
    """
    Generates a random number in the given range.
    
    parameters:
        max: type=int
            max value of random number
        min: type=int
            min value of random number

    returns: type=int
        A random number
    """
    return random.random() * max + min

def randomDataThread(args):
    """
    Thread that updates testPlot module with random data every second
    """
    while not args['done']:
        points = 100
        ys = [ generateRandomNumber() for y in range(points) ] # time domain samples
        xs = [ t for t in range(points) ] # time domain samples

        testPlot.xs = xs
        testPlot.ys = ys
        time.sleep(0.1)