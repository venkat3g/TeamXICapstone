import threading
import PlutoController
import testPlot
import time


collectionThread = None
collectionThreadArgs = {'done': False}

def start(threadFunction):
    global collectionThread
    if collectionThread is None:
        collectionThread = threading.Thread(target=threadFunction, args=[collectionThreadArgs])
        collectionThread.start()
    else:
        print("Collection thread has already started")

def stop():
    collectionThreadArgs['done'] = True
    collectionThread.join()

