import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
from matplotlib.widgets import Button
from matplotlib import style
import random
from scipy import signal as sig
import PlutoController

style.use('fivethirtyeight')

_animation_period = 10000

playing = True
rxData = None
txData = None
plot_fir = False
freq_dom = False
compl = False
rxImaginary = False
txImaginary = False
PLOT_COLOURS = ('b', 'r')

def get_animation_period():
        return _animation_period / 1e3


def set_animation_period(value):
        global _animation_period
        _animation_period = value * 1e3 # convert seconds to milliseconds

def toggle(evnt):
        global playing, ani
        if playing:
                ani.event_source.stop()
        else:
                ani.event_source.start()
        playing = not playing

def openWindow():
        global fig, ax1, ax2
        fig = plt.figure()
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        setupCanvas()

def handle_close(evnt):
        pass

def setupCanvas():
        global fig, ax1, ani
        ani = animation.FuncAnimation(fig, animate, interval=_animation_period)
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
        global fig, ax1, ax2, xs, ys
        ax1.clear()
        ax2.clear()
        ani.event_source.interval = _animation_period
        
        if plot_fir and rxData is not None:
                fir_plot(rxData)

        if rxData is not None:
                ax1.set_title("Receiving")
                if PlutoController.rxPlotList[PlutoController.rxPlotIndex] == 'Time':
                        rawRXData = PlutoController.getSdr().complex2raw(rxData, 16)
                        ax1.plot(rawRXData[0::2], PLOT_COLOURS[1])
                        if rxImaginary:
                                ax1.plot(rawRXData[1::2])

                elif PlutoController.rxPlotList[PlutoController.rxPlotIndex] == 'Frequency':
                        xs = [x.real for x in rxData]
                        ys = [x.imag for x in rxData]

                        ax1.semilogy(xs, ys)

                elif PlutoController.rxPlotList[PlutoController.rxPlotIndex] == 'Constellation (X vs Y)':
                        xs = [x.real for x in rxData]
                        ys = [x.imag for x in rxData]

                        # ax1.axis([-1, 1, -1, 1])
                        ax1.plot(xs, ys, 'o')

        if txData is not None:
                ax2.set_title("Transmition")
                if PlutoController.txPlotList[PlutoController.txPlotIndex] == 'Time':
                        rawTXData = PlutoController.getSdr().complex2raw(txData, 16)
                        ax2.plot(rawTXData[0::2], PLOT_COLOURS[1])
                        if txImaginary:
                                ax2.plot(rawTXData[1::2])

                elif PlutoController.txPlotList[PlutoController.txPlotIndex] == 'Frequency':
                        xs = [x.real for x in txData]
                        ys = [x.imag for x in txData]

                        ax2.semilogy(xs, ys)

                elif PlutoController.txPlotList[PlutoController.txPlotIndex] == 'Constellation (X vs Y)':
                        xs = [x.real for x in txData]
                        ys = [x.imag for x in txData]

                        # ax2.axis([-1, 1, -1, 1])
                        ax2.plot(xs, ys, 'o')

