if __name__ == "__main__":
    from gui import plutoPage as deviceInfoPage
    from gui import testPlot, PlutoController
    from gui.ThreadWrapper import ThreadController
    import logging
    import os
    import multiprocessing
    
    multiprocessing.freeze_support()

    filename = 'pluto.log'
    i = 0
    while os.path.isfile(filename):
        i = i + 1
        filename = 'pluto' + str(i) + '.log'

    # logging.basicConfig(filename=filename, level=logging.DEBUG)

    PlutoController.readRX = True
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