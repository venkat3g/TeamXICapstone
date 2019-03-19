import sys
import PlutoConfig
import PlutoController
import PlutoConfig_support
import testPlot
import launchTTT

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
playerNumber = 1

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global root, top
    root = tk.Tk()
    root.withdraw()
    (w, top) = PlutoConfig.create_TopLevel(root)

    addMenubar(w)
    addGUIContent()

    # Set Bindings for updates
    top.SaveButton.bind('<ButtonRelease-1>', update)
    top.TXDataFileButton.bind('<ButtonRelease-1>', pickFile)

    w.protocol("WM_DELETE_WINDOW", root.quit)

def pickFile(evnt):
    file_path = fileDialog.askopenfilename()
    PlutoConfig_support.txDataFile.set(file_path)
    PlutoController.updateMsgToSend(file_path)
    

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

    # Modulation Scheme Drop-down
    modScheme = tk.StringVar()
    modScheme.set(PlutoController.ModulationFactory.QAM)
    
    popupMenu = tk.OptionMenu(top.ModulationSchemeFrame, modScheme, *PlutoController.ModulationFactory.SUPPORTED_SCHEMES)
    popupMenu.place(relx=0.5, rely=0.25)

    # Set Bindings for updates
    gainMode.trace("w", lambda *args: PlutoController.updateGainMode(gainMode.get().upper()))
    rxPlot.trace("w", lambda *args: PlutoController.updateRXPlot(rxPlot.get()))
    txPlot.trace("w", lambda *args: PlutoController.updateTXPlot(txPlot.get()))
    modScheme.trace("w", lambda *args: PlutoController.updateModScheme(modScheme.get()))
    
    # add bindings for checkboxes
    PlutoConfig_support.rxImaginary.trace('w', lambda *args: PlutoController.updateRXImaginary(PlutoConfig_support.rxImaginary.get()))
    PlutoConfig_support.txImaginary.trace('w', lambda *args: PlutoController.updateTXImaginary(PlutoConfig_support.txImaginary.get()))
    PlutoConfig_support.txOn.trace('w', lambda *args: PlutoController.setTXStatus(PlutoConfig_support.txOn.get()))
    

def addMenubar(w):
    menubar = tk.Menu(root)
    sub_menu = tk.Menu(root, tearoff=0)
    menubar.add_cascade(menu=sub_menu, label="Games")
    menubar.add_command(label="Show Plot", command=testPlot.openWindow)
    
    sub_menu.add_command(label="Tic-Tac-Toe", command=startTicTacToe)
    sub_menu.add_radiobutton(label="Player 1", command=setPlayerOne)
    sub_menu.add_radiobutton(label="Player 2", command=setPlayerTwo)

    w.config(menu=menubar)
    
def setPlayerOne():
    global playerNumber
    playerNumber = 1

def setPlayerTwo():
    global playerNumber
    playerNumber = 2

def startTicTacToe():
    PlutoController.sendMsg("") # Clear all prior messages
    launchTTT.startTicTacToe(root, playerNumber)

def update(evnt):

    # Update Back-end
    PlutoController.threadPeriod = float(PlutoConfig_support.threadUpdate.get())
    testPlot.set_animation_period(float(PlutoConfig_support.plotUpdate.get()))

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

    # Update PulseShaping Filter Values
    D = int(PlutoConfig_support.pulseShapingD.get())
    P = int(PlutoConfig_support.pulseShapingP.get())
    alpha = float(PlutoConfig_support.pulseShapingAlpha.get())
    PlutoController.updatePulseShapingFilter(D=D, P=P, alpha=alpha)
    desiredBandwidth = float(PlutoConfig_support.desiredBandwidth.get())
    PlutoController.updateDesiredBandwidth(desiredBandwidth)

    # Calculate Sampling Frequency from P, alpha and desiredBandwidth
    # and set Pluto's sampling_frequency
    PlutoController.getSdr().sampling_frequency = P * desiredBandwidth / (1 + alpha)

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

    PlutoConfig_support.rxImaginary.set(PlutoController.getRXImaginary())
    PlutoConfig_support.txImaginary.set(PlutoController.getTXImaginary())
    PlutoConfig_support.txOn.set(PlutoController.getTXStatus())
    
    # Update Pulse Shaping Values
    (D, P, alpha) = PlutoController.getPulseShapingValues()
    PlutoConfig_support.pulseShapingD.set(D)
    PlutoConfig_support.pulseShapingP.set(P)
    PlutoConfig_support.pulseShapingAlpha.set(alpha)
    PlutoConfig_support.desiredBandwidth.set(PlutoController.getDesiredBandwidth())

def loadGUIItems():
    global ctx
    ctx = PlutoController.getIIOContext()

    top.ContextName.configure(text="Context Type: " + ctx.name)
    top.ContextName.pack()
    updateGUI()

def vp_start_loop():
    root.mainloop()