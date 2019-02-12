import sys
import PlutoConfig
import PlutoController
import PlutoConfig_support
import testPlot

try:
    import Tkinter as tk
    import tkFileDialog as fileDialog
except ImportError:
    import tkinter as tk
    from tkinter import fileDialog
    

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


ctx = None
top = None

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global root, top, rxPlot, txPlot, RXPlotOptionMenu, TXPlotOptionMenu
    root = tk.Tk()
    root.withdraw()
    (w, top) = PlutoConfig.create_TopLevel(root)

    addGUIContent()

    # Set Bindings for updates
    top.SaveButton.bind('<ButtonRelease-1>', update)
    top.TXDataFileButton.bind('<ButtonRelease-1>', pickFile)

    w.protocol("WM_DELETE_WINDOW", root.quit)

def pickFile(evnt):
    file_path = fileDialog.askopenfilename()
    PlutoConfig_support.txDataFile.set(file_path)
    

def addGUIContent():
    gainMode = tk.StringVar()
    gainMode.set(PlutoController.rxGainModes[PlutoController.rxGainModeIndex])
    PlutoController.getSdr().rx_gain_mode = gainMode.get().upper()

    RXGainModeOptionMenu = apply(tk.OptionMenu, (top.RXGainModeFrame, gainMode) + tuple(PlutoController.rxGainModes))
    RXGainModeOptionMenu.pack()

    rxPlot = tk.StringVar()
    rxPlot.set(PlutoController.rxPlotList[PlutoController.rxPlotIndex])

    RXPlotOptionMenu = apply(tk.OptionMenu, (top.RXPlotFrame, rxPlot) + tuple(PlutoController.rxPlotList))
    RXPlotOptionMenu.pack()

    txPlot = tk.StringVar()
    txPlot.set(PlutoController.txPlotList[PlutoController.txPlotIndex])

    TXPlotOptionMenu = apply(tk.OptionMenu, (top.TXPlotFrame, txPlot) + tuple(PlutoController.txPlotList))
    TXPlotOptionMenu.pack()

    # Set Bindings for updates
    gainMode.trace("w", lambda *args: PlutoController.updateGainMode(gainMode.get().upper()))
    rxPlot.trace("w", lambda *args: PlutoController.updateRXPlot(rxPlot.get()))
    txPlot.trace("w", lambda *args: PlutoController.updateTXPlot(txPlot.get()))

def update(evnt):

    # Update Back-end
    PlutoController.threadPeriod = float(PlutoConfig_support.threadUpdate.get())
    testPlot.set_animation_period(float(PlutoConfig_support.plotUpdate.get()))

    # Update PlutoSDR
    PlutoController.getSdr().sampling_frequency = float(PlutoConfig_support.samplingFrequency.get())

    # Update PlutoSDR using RX Frame information
    PlutoController.rxSamples = int(PlutoConfig_support.rxSamples.get())
    PlutoController.getSdr().rx_bandwidth = float(PlutoConfig_support.rxBandwidth.get())
    PlutoController.getSdr().rx_lo_freq = float(PlutoConfig_support.rxFrequency.get())
    # TODO update decimation
    PlutoController.getSdr().rx_gain = float(PlutoConfig_support.rxGain.get())
    
    # Update PlutoSDR using TX Frame information
    PlutoController.getSdr().tx_lo_freq = float(PlutoConfig_support.txFrequency.get())
    PlutoController.getSdr().tx_bandwidth = float(PlutoConfig_support.txBandwidth.get())
    PlutoController.txSamples = int(PlutoConfig_support.txSamples.get())
    # TODO update interpolation
    PlutoController.getSdr().tx_gain = float(PlutoConfig_support.txGain.get())

    updateGUI()

def updateGUI():
    PlutoConfig_support.samplingFrequency.set(PlutoController.getSdr().sampling_frequency)
    PlutoConfig_support.threadUpdate.set(PlutoController.threadPeriod)
    PlutoConfig_support.plotUpdate.set(testPlot.get_animation_period())

    # Update RX Frame information
    PlutoConfig_support.rxFrequency.set(PlutoController.getSdr().rx_lo_freq)
    PlutoConfig_support.rxBandwidth.set(PlutoController.getSdr().rx_bandwidth)
    PlutoConfig_support.rxDecimation.set(PlutoController.getSdr().rx_decimation)
    PlutoConfig_support.rxGain.set(PlutoController.getSdr().rx_gain)    
    PlutoConfig_support.rxSamples.set(PlutoController.rxSamples)

    # Update TX Frame information
    PlutoConfig_support.txFrequency.set(PlutoController.getSdr().tx_lo_freq)
    PlutoConfig_support.txBandwidth.set(PlutoController.getSdr().tx_bandwidth)
    PlutoConfig_support.txInterpolation.set(PlutoController.getSdr().tx_interpolation)
    PlutoConfig_support.txGain.set(PlutoController.getSdr().tx_gain)
    PlutoConfig_support.txDataFile.set(PlutoController.txDataFile)
    PlutoConfig_support.txSamples.set(PlutoController.txSamples)
    

def loadGUIItems():
    global ctx
    ctx = PlutoController.getIIOContext()

    top.ContextName.configure(text="Context Type: " + ctx.name)
    top.ContextName.pack()
    updateGUI()

def vp_start_loop():
    root.mainloop()