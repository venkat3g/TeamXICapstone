import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
from matplotlib.widgets import Button
from matplotlib import style
import random
from scipy import signal as sig

style.use('fivethirtyeight')

playing = True
xs = []
ys = []
rxData = None
plot_fir = False
PLOT_COLOURS = ('b', 'r')

def toggle(evnt):
        global playing, ani
        if playing:
                ani.event_source.stop()
        else:
                ani.event_source.start()
        playing = not playing

def openWindow():
        global fig, ax1
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        setupCanvas()

def handle_close(evnt):
        pass

def setupCanvas():
        global fig, ax1, ani
        ani = animation.FuncAnimation(fig, animate, interval=1000)
        plt.show()
        fig.canvas.mpl_connect('close_event', handle_close)

def fir_plot(rxData, a=1, grid=True, phase=False):
        """
        Plots FIR
        """
        global fig, ax1, ani
        w, h = sig.freqz(rxData, a)
        w_norm = w/max(w)
        ax1.plot(w_norm, 20*np.log10(np.abs(h)), PLOT_COLOURS[0])
        plt.title('FIR Frequency Response')
        plt.xlabel('Normalised Frequency [rads/sample]')
        plt.ylabel('Amplidude [dB]', color=PLOT_COLOURS[0])
        if phase:
                ax2 = ax1.twinx()
                rads = np.unwrap(np.angle(h))
                ax1.plot(w_norm, rads, PLOT_COLOURS[1])
                plt.ylabel('Phase [rads/sample]', color=PLOT_COLOURS[1])
        if grid:
                plt.grid()
        #plt.axis('tight')
        # plt.show()

def animate(i):
        global fig, ax1, xs, ys
        ax1.clear()
        # plt.ylabel('Imaginary')
        # plt.xlabel('Real')
        # plt.axis([-.2, .2, -.2, .2])
        # ax1.plot(xs, ys, 'o')
        if fir_plot == False or rxData is None:
                ax1.plot(xs, ys)
        else:
                fir_plot(rxData)

