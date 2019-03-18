import threading
import PlutoController
import testPlot
import time

class ThreadController:
    def __init__(self, threadFunction):
        self.threadFunction = threadFunction
        self.collectionThread = None
        self.collectionThreadArgs = {'done': False}

    def start(self):
        if self.collectionThread is None:
            self.collectionThread = threading.Thread(target=self.threadFunction, args=[self.collectionThreadArgs])
            self.collectionThread.start()
        else:
            print("Collection thread has already started")

    def stop(self):
        self.collectionThreadArgs['done'] = True
        self.collectionThread.join()

