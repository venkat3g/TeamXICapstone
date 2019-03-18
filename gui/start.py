import plutoPage as deviceInfoPage
import testPlot
import PlutoController
from ThreadWrapper import ThreadController
import logging
import os


filename = 'pluto.log'
i = 0
while os.path.isfile(filename):
    i = i + 1
    filename = 'pluto' + str(i) + '.log'

# logging.basicConfig(filename=filename, level=logging.DEBUG)

PlutoController.rx_show_all_plots = False

if PlutoController.rx_show_all_plots:
    PlutoController.configure(2400, 3, 10)

if not PlutoController.rx_show_all_plots:
    deviceInfoPage.vp_start_gui()
    deviceInfoPage.loadGUIItems()

collectionThread = ThreadController(PlutoController.plutoRXThread)

collectionThread.start()

if not PlutoController.rx_show_all_plots:
    testPlot.openWindow()

    deviceInfoPage.vp_start_loop()

    collectionThread.stop()

print("done")