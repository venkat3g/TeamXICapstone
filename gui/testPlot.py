import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
from matplotlib.widgets import Button
from matplotlib import style
import random

style.use('fivethirtyeight')

playing = True
xs = []
ys = []

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

def animate(i):
        global fig, ax1, xs, ys
        ax1.clear()
        ax1.plot(xs, ys)

