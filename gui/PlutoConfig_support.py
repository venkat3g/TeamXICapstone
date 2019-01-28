#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Jan 30, 2019 12:33:43 AM EST  platform: Windows NT

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
    global rxSamplingFrequency
    rxSamplingFrequency = tk.StringVar()
    global rxSamples
    rxSamples = tk.StringVar()
    global txFrequency
    txFrequency = tk.StringVar()
    global txBandwidth
    txBandwidth = tk.StringVar()

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




