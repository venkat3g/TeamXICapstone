import plutoPage as deviceInfoPage
import iio_xmlInfo
import testPlot
import PlutoController
import CollectionThread



deviceInfoPage.vp_start_gui()

PlutoController.configure(2400, 30)

deviceInfoPage.loadGUIItems()

CollectionThread.start()

testPlot.openWindow()

deviceInfoPage.vp_start_loop()

CollectionThread.stop()

print("done")