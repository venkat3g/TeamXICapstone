import sys
import mainpage
import PlutoController
import testPlot

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

def openTestCanvas(evt):
    testPlot.openWindow()

ctx = None
top = None

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global root, top
    root = tk.Tk()
    root.withdraw()
    (w, top) = mainpage.create_TopLevel(root)

    top.Switch.bind('<Button-1>', openTestCanvas)

    w.protocol("WM_DELETE_WINDOW", root.quit)    

def updateGUI(deviceIndex):
    # Clear all existing items
    top.Channels.delete(0, tk.END)
    top.Attrs.delete(0, tk.END)
    top.DebugAttrs.delete(0, tk.END)

    for channel in ctx.devices[deviceIndex].channels:
        top.Channels.insert(tk.END, str(channel.name))

    for debug_attr in ctx.devices[deviceIndex].debug_attrs:
        top.DebugAttrs.insert(tk.END, str(debug_attr))

    for attr in ctx.devices[deviceIndex].attrs:
        top.Attrs.insert(tk.END, str(attr))

def onDeviceSelect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    updateGUI(index)

def loadGUIItems():
    global ctx
    ctx = PlutoController.getIIOContext()

    top.IIO_Context.configure(text="Context Type: " + ctx.name)
    top.IIO_Context.pack()

    for dev in ctx.devices:
        top.Devices.insert(tk.END, str(dev.name))

    top.Devices.bind('<<ListboxSelect>>', onDeviceSelect)

def vp_start_loop():
    root.mainloop()