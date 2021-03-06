#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Apr 02, 2019 11:19:01 PM EDT  platform: Windows NT
#    Apr 11, 2019 05:16:28 PM EDT  platform: Windows NT
#    Apr 12, 2019 04:03:15 PM EDT  platform: Windows NT
#    Apr 15, 2019 11:56:42 PM EDT  platform: Windows NT

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
    global vpr_value
    vpr_value = tk.StringVar()
    vpr_value.set('...')
    global throughput_value
    throughput_value = tk.StringVar()
    throughput_value.set('...')
    global processingTime_value
    processingTime_value = tk.StringVar()
    processingTime_value.set('...')
    global perPacket_value
    perPacket_value = tk.StringVar()
    perPacket_value.set('...')
    global tThroughput_value
    tThroughput_value = tk.StringVar()
    tThroughput_value.set('...')
    global tPerPacket_value
    tPerPacket_value = tk.StringVar()
    tPerPacket_value.set('...')
    global validPackets_value
    validPackets_value = tk.StringVar()
    validPackets_value.set('...')
    global totalPackets_value
    totalPackets_value = tk.StringVar()
    totalPackets_value.set('...')
    global msgSize_value
    msgSize_value = tk.StringVar()
    global guiUpdate_value
    guiUpdate_value = tk.StringVar()
    global adjustedRXSamples_value
    adjustedRXSamples_value = tk.StringVar()
    adjustedRXSamples_value.set('...')
    global startingRXSample_value
    startingRXSample_value = tk.StringVar()
    global dynamicAdjust
    dynamicAdjust = tk.StringVar()
    global transmit
    transmit = tk.StringVar()
    global correct_frequency
    correct_frequency = tk.StringVar()

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
    import Throughput
    Throughput.vp_start_gui()




