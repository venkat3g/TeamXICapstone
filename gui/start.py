import deviceInfo as deviceInfoPage
import iio_xmlInfo

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

def updateGUI(deviceIndex):
    # Clear all existing items
    deviceInfoPage.top.Channels.delete(0, END)
    deviceInfoPage.top.Attrs.delete(0, END)
    deviceInfoPage.top.DebugAttrs.delete(0, END)

    for channel in ctx.devices[deviceIndex].channels:
        deviceInfoPage.top.Channels.insert(END, str(channel.name))

    for debug_attr in ctx.devices[deviceIndex].debug_attrs:
        deviceInfoPage.top.DebugAttrs.insert(END, str(debug_attr))
    
    for attr in ctx.devices[deviceIndex].attrs:
        deviceInfoPage.top.Attrs.insert(END, str(attr))

def onDeviceSelect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    updateGUI(index)
    

deviceInfoPage.vp_start_gui()

ctx = iio_xmlInfo.getIIOContext()

deviceInfoPage.top.IIO_Context.configure(text="Context Type: " + ctx.name)
deviceInfoPage.top.IIO_Context.pack()

for dev in ctx.devices:
    deviceInfoPage.top.Devices.insert(END, str(dev.name))

deviceInfoPage.top.Devices.bind('<<ListboxSelect>>', onDeviceSelect)

deviceInfoPage.vp_start_loop()