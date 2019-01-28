import randomData
import threading
import PlutoController
import testPlot
import time


collectionThread = None
collectionThreadArgs = {'done': False}

def start():
    global collectionThread
    if collectionThread is None:
        collectionThread = threading.Thread(target=PlutoController.plutoRXThread, args=[collectionThreadArgs])
        collectionThread.start()
    else:
        print("Collection thread has already started")

def stop():
    collectionThreadArgs['done'] = True
    collectionThread.join()

