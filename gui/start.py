import plutoPage as deviceInfoPage
import iio_xmlInfo
import testPlot
import PlutoController
import randomData
import CollectionThread
import logging
import os


filename = 'pluto.log'
i = 0
while os.path.isfile(filename):
    i = i + 1
    filename = 'pluto' + str(i) + '.log'

# logging.basicConfig(filename=filename, level=logging.DEBUG)

deviceInfoPage.vp_start_gui()

# PlutoController.configure(2400, 3, 10)

deviceInfoPage.loadGUIItems()

CollectionThread.start(PlutoController.plutoRXThread)

testPlot.openWindow()

deviceInfoPage.vp_start_loop()

CollectionThread.stop()

print("done")