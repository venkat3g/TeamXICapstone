#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Jan 24, 2019 10:05:10 AM EST  platform: Windows NT

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

import mainpage_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = TopLevel (root)
    mainpage_support.init(root, top)
    root.mainloop()

w = None
def create_TopLevel(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = TopLevel (w)
    mainpage_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_TopLevel():
    global w
    w.destroy()
    w = None

class TopLevel:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#ececec' # Closest X11 color: 'gray92' 
        font9 = "-family {Segoe UI} -size 24 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("681x540+650+150")
        top.title("New Toplevel")
        top.configure(background="#ffffff")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.IIO_Context = tk.Label(top)
        self.IIO_Context.place(relx=0.294, rely=0.0, height=54, width=211)
        self.IIO_Context.configure(activebackground="#f9f9f9")
        self.IIO_Context.configure(activeforeground="black")
        self.IIO_Context.configure(background="#ffffff")
        self.IIO_Context.configure(disabledforeground="#a3a3a3")
        self.IIO_Context.configure(font=font9)
        self.IIO_Context.configure(foreground="#000000")
        self.IIO_Context.configure(highlightbackground="#d9d9d9")
        self.IIO_Context.configure(highlightcolor="black")
        self.IIO_Context.configure(text='''Context''')

        self.DeviceFrame = tk.LabelFrame(top)
        self.DeviceFrame.place(relx=0.0, rely=0.093, relheight=0.2, relwidth=1.0)

        self.DeviceFrame.configure(relief='groove')
        self.DeviceFrame.configure(foreground="black")
        self.DeviceFrame.configure(text='''Devices''')
        self.DeviceFrame.configure(background="#d9d9d9")
        self.DeviceFrame.configure(highlightbackground="#d9d9d9")
        self.DeviceFrame.configure(highlightcolor="black")
        self.DeviceFrame.configure(width=320)

        self.Devices = ScrolledListBox(self.DeviceFrame)
        self.Devices.place(relx=0.0, rely=0.185, relheight=0.796, relwidth=1.0
                , bordermode='ignore')
        self.Devices.configure(background="white")
        self.Devices.configure(disabledforeground="#a3a3a3")
        self.Devices.configure(font="TkFixedFont")
        self.Devices.configure(foreground="black")
        self.Devices.configure(highlightbackground="#d9d9d9")
        self.Devices.configure(highlightcolor="#d9d9d9")
        self.Devices.configure(selectbackground="#c4c4c4")
        self.Devices.configure(selectforeground="black")
        self.Devices.configure(selectmode='single')
        self.Devices.configure(width=10)

        self.AttrFrame = tk.LabelFrame(top)
        self.AttrFrame.place(relx=0.0, rely=0.537, relheight=0.2, relwidth=1.0)
        self.AttrFrame.configure(relief='groove')
        self.AttrFrame.configure(foreground="black")
        self.AttrFrame.configure(text='''Attributes''')
        self.AttrFrame.configure(background="#d9d9d9")
        self.AttrFrame.configure(highlightbackground="#d9d9d9")
        self.AttrFrame.configure(highlightcolor="black")
        self.AttrFrame.configure(width=320)

        self.Attrs = ScrolledListBox(self.AttrFrame)
        self.Attrs.place(relx=0.0, rely=0.185, relheight=0.796, relwidth=1.0
                , bordermode='ignore')
        self.Attrs.configure(background="white")
        self.Attrs.configure(disabledforeground="#a3a3a3")
        self.Attrs.configure(font="TkFixedFont")
        self.Attrs.configure(foreground="black")
        self.Attrs.configure(highlightbackground="#d9d9d9")
        self.Attrs.configure(highlightcolor="#d9d9d9")
        self.Attrs.configure(selectbackground="#c4c4c4")
        self.Attrs.configure(selectforeground="black")
        self.Attrs.configure(selectmode='single')
        self.Attrs.configure(width=10)

        self.DebugAttrsFrame = tk.LabelFrame(top)
        self.DebugAttrsFrame.place(relx=0.0, rely=0.741, relheight=0.2
                , relwidth=1.0)
        self.DebugAttrsFrame.configure(relief='groove')
        self.DebugAttrsFrame.configure(foreground="black")
        self.DebugAttrsFrame.configure(text='''Debug Attributes''')
        self.DebugAttrsFrame.configure(background="#d9d9d9")
        self.DebugAttrsFrame.configure(highlightbackground="#d9d9d9")
        self.DebugAttrsFrame.configure(highlightcolor="black")
        self.DebugAttrsFrame.configure(width=320)

        self.DebugAttrs = ScrolledListBox(self.DebugAttrsFrame)
        self.DebugAttrs.place(relx=0.0, rely=0.185, relheight=0.796, relwidth=1.0
                , bordermode='ignore')
        self.DebugAttrs.configure(background="white")
        self.DebugAttrs.configure(disabledforeground="#a3a3a3")
        self.DebugAttrs.configure(font="TkFixedFont")
        self.DebugAttrs.configure(foreground="black")
        self.DebugAttrs.configure(highlightbackground="#d9d9d9")
        self.DebugAttrs.configure(highlightcolor="#d9d9d9")
        self.DebugAttrs.configure(selectbackground="#c4c4c4")
        self.DebugAttrs.configure(selectforeground="black")
        self.DebugAttrs.configure(selectmode='single')
        self.DebugAttrs.configure(width=10)

        self.ChannelFrame = tk.LabelFrame(top)
        self.ChannelFrame.place(relx=0.0, rely=0.315, relheight=0.2
                , relwidth=1.0)
        self.ChannelFrame.configure(relief='groove')
        self.ChannelFrame.configure(foreground="black")
        self.ChannelFrame.configure(text='''Channels''')
        self.ChannelFrame.configure(background="#d9d9d9")
        self.ChannelFrame.configure(highlightbackground="#d9d9d9")
        self.ChannelFrame.configure(highlightcolor="black")
        self.ChannelFrame.configure(width=320)

        self.Channels = ScrolledListBox(self.ChannelFrame)
        self.Channels.place(relx=0.0, rely=0.185, relheight=0.796, relwidth=1.0
                , bordermode='ignore')
        self.Channels.configure(background="white")
        self.Channels.configure(disabledforeground="#a3a3a3")
        self.Channels.configure(font="TkFixedFont")
        self.Channels.configure(foreground="black")
        self.Channels.configure(highlightbackground="#d9d9d9")
        self.Channels.configure(highlightcolor="#d9d9d9")
        self.Channels.configure(selectbackground="#c4c4c4")
        self.Channels.configure(selectforeground="black")
        self.Channels.configure(selectmode='single')
        self.Channels.configure(width=10)

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                  + tk.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, tk.Listbox):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')

if __name__ == '__main__':
    vp_start_gui()





