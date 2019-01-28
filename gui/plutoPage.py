import sys
import PlutoConfig
import PlutoController
import PlutoConfig_support

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

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
    global root, top
    root = tk.Tk()
    root.withdraw()
    (w, top) = PlutoConfig.create_TopLevel(root)
    w.protocol("WM_DELETE_WINDOW", root.quit)    

def updateRX(evnt):
    # Update PlutoSDR using RX Frame information
    PlutoController.rxSamples = int(PlutoConfig_support.rxSamples.get())
    PlutoController.getSdr().rx_bandwidth = float(PlutoConfig_support.rxBandwidth.get())
    PlutoController.getSdr().sampling_frequency = float(PlutoConfig_support.rxSamplingFrequency.get())
    PlutoController.getSdr().rx_lo_freq = float(PlutoConfig_support.rxFrequency.get())
    updateGUI()

def updateTX(evnt):
    # Update PlutoSDR using TX Frame information
    PlutoController.getSdr().tx_lo_freq = float(PlutoConfig_support.txFrequency.get())
    PlutoController.getSdr().tx_bandwidth = float(PlutoConfig_support.txBandwidth.get())
    updateGUI()

def updateGUI():
    PlutoConfig_support.rxSamples.set(PlutoController.rxSamples)
    # Update RX Frame information
    PlutoConfig_support.rxBandwidth.set(PlutoController.getSdr().rx_bandwidth)
    PlutoConfig_support.rxSamplingFrequency.set(PlutoController.getSdr().sampling_frequency)
    PlutoConfig_support.rxFrequency.set(PlutoController.getSdr().rx_lo_freq)

    # Update TX Frame information
    PlutoConfig_support.txFrequency.set(PlutoController.getSdr().tx_lo_freq)
    PlutoConfig_support.txBandwidth.set(PlutoController.getSdr().tx_bandwidth)

    # Set Bindings for updates
    top.RXSaveButton.bind('<ButtonRelease-1>', updateRX)
    top.TXSaveButton.bind('<ButtonRelease-1>', updateTX)

def loadGUIItems():
    global ctx
    ctx = PlutoController.getIIOContext()

    top.ContextName.configure(text="Context Type: " + ctx.name)
    top.ContextName.pack()
    updateGUI()

def vp_start_loop():
    root.mainloop()