#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Mar 07, 2019 01:35:30 PM EST  platform: Windows NT

import sys

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

def set_Tk_var():
    global rxBandwidth
    rxBandwidth = tk.StringVar()
    global rxFrequency
    rxFrequency = tk.StringVar()
    global rxSamples
    rxSamples = tk.StringVar()
    global rxDecimation
    rxDecimation = tk.StringVar()
    global rxGain
    rxGain = tk.StringVar()
    global rxImaginary
    rxImaginary = tk.StringVar()
    global txFrequency
    txFrequency = tk.StringVar()
    global txBandwidth
    txBandwidth = tk.StringVar()
    global txSamples
    txSamples = tk.StringVar()
    global txInterpolation
    txInterpolation = tk.StringVar()
    global txGain
    txGain = tk.StringVar()
    global txDataFile
    txDataFile = tk.StringVar()
    global txImaginary
    txImaginary = tk.StringVar()
    global txOn
    txOn = tk.StringVar()
    global samplingFrequency
    samplingFrequency = tk.StringVar()
    global threadUpdate
    threadUpdate = tk.StringVar()
    global plotUpdate
    plotUpdate = tk.StringVar()
    global pulseShapingD
    pulseShapingD = tk.StringVar()
    global pulseShapingP
    pulseShapingP = tk.StringVar()
    global pulseShapingAlpha
    pulseShapingAlpha = tk.StringVar()
    global desiredBandwidth
    desiredBandwidth = tk.StringVar()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import PlutoConfig
    PlutoConfig.vp_start_gui()




