# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 18:07:59 2021

@author: USER
"""
import copy
import time
import math
import numpy as np
import pickle
import cv2
import socket
import sys

import matplotlib.pyplot as plt
from get_cam_num import camera_num

# from IPython import get_ipython
# get_ipython().run_line_magic('matplotlib', 'qt')
plt.ion()

buf_socket_rx = []
for i in range(camera_num):
    buf_socket_rx.append([])
for i in range(camera_num):
    buf_socket_rx[i].append(0xAA)
    for j in range((24 * 32)):
        buf_socket_rx[i].append(0x00)
    buf_socket_rx[i].append(0xBB)

print_mode = 0  # 0 = temperture # 1 = ascii

min_temp = 15.00
max_temp = 35.00

temperature = np.zeros([camera_num, 24, 32])
# heatmap = np.zeros([24*8,32*8,3])


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# Qt: v 5.9.7 	PyQt: v 5.9.2
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# matplotlib.__version__ 3.4.3

# app = QApplication([])

thread = QThread()

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Worker(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)

    def get_temperature(self):
        global ClientSocket
        global buf_socket_rx
        global temperature
        # global canvas, chart

        ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_host = '192.168.0.22'
        server_port = 9999

        rx_array = []

        fps = 0
        now_time = time.time()
        while True:
            try:
                ClientSocket.connect((server_host, server_port))

                rx_time_out = time.time()
                while True:
                    rx_char = ClientSocket.recv(1)
                    if len(rx_char) != 0:
                        rx_array.append(rx_char[0])
                        # print(rx_char[0])
                        rx_time_out = time.time()

                    if len(rx_array) >= (2 * ((24 * 32) + 1 + 2)):
                        if (rx_array[0] * 0x10 + rx_array[1]) == 0xAA and (
                                rx_array[2 * ((24 * 32) + 1 + 1)] * 0x10 + rx_array[
                            2 * ((24 * 32) + 1 + 1) + 1]) == 0xBB and (
                                rx_array[2 * ((24 * 32) + 1)] * 0x10 + rx_array[2 * ((24 * 32) + 1) + 1]) <= 0b1111:
                            # tempture <- rx_array
                            # print((rx_array[2*((24*32)+1)] * 0x10 + rx_array[2*((24*32)+1) + 1]))
                            # print(time.time())

                            slave_address = (rx_array[2 * ((24 * 32) + 1)] * 0x10 + rx_array[2 * ((24 * 32) + 1) + 1])
                            for i in range(24 * 32):
                                buf_socket_rx[slave_address][1 + i] = (
                                            rx_array[2 * (1 + i)] * 0x10 + rx_array[2 * (1 + i) + 1])

                            for h in range(24):
                                for w in range(32):
                                    # temperature[h,w] = (float(buf_socket_rx[0][1+(h*32 + w)])) - 40.0;
                                    temperature[slave_address][h, w] = (float(
                                        buf_socket_rx[slave_address][1 + (h * 32 + w)])) - 40.0;

                            if slave_address == 0b0000:
                                fps = (0.5 * fps) + (0.5 * (1 / (time.time() - now_time)))
                                print(str(fps))
                                now_time = time.time()

                            rx_array = []
                        else:
                            rx_array = rx_array[1:]

                    if time.time() > (rx_time_out + 60.0):
                        break

                ClientSocket.close()
            except:
                print('No reponse from server: ' + str(server_host) + ':' + str(server_port))
                time.sleep(1.0)

                if time.time() > (rx_time_out + 60.0):
                    ClientSocket.close()
                    break


###worker2 start
thread_draw_chart = QThread()

### Drawing Canvas
canvas = []
chart = []

for i in range(camera_num):
    canvas.append(FigureCanvas(Figure(figsize=(10, 6),tight_layout=True)))
    chart.append(canvas[i].figure.add_subplot())

    heatmap_zero = np.zeros((24 * 8, 32 * 8))

    chart[i].clear()
    chart[i].get_xaxis().set_visible(False)
    chart[i].get_yaxis().set_visible(False)
    chart[i].imshow(heatmap_zero, cmap='jet', vmin=min_temp, vmax=max_temp)

    # print("canvas ", i , "생성")
    canvas[i].draw()

child_canvas = []
child_chart = []
for i in range(camera_num):
    child_canvas.append(FigureCanvas(Figure(figsize=(10, 6),tight_layout=True)))
    child_chart.append(child_canvas[i].figure.add_subplot())

    child_chart[i].clear()
    child_chart[i].get_xaxis().set_visible(False)
    child_chart[i].get_yaxis().set_visible(False)
    child_chart[i].imshow(heatmap_zero, cmap='jet', vmin=min_temp, vmax=max_temp)

    # print("canvas ", i , "생성")
    child_canvas[i].draw()

class Worker2(QObject):
    def __init__(self, parent=None, camera_num = camera_num):
        QObject.__init__(self, parent=parent)
        self.camera_num = camera_num


    def display_plot(self):
        while True:
            try:
                for i in range(camera_num):
                    self.temperature_upscale = cv2.resize(temperature[i], None, fx=8, fy=8, interpolation=cv2.INTER_CUBIC)
                    self.temperature_upscale = cv2.flip(self.temperature_upscale, 1)

                    chart[i].clear()

                    chart[i].get_xaxis().set_visible(False)
                    chart[i].get_yaxis().set_visible(False)
                    chart[i].imshow(self.temperature_upscale, cmap='jet', vmin=min_temp, vmax=max_temp)

                    canvas[i].draw()

                    ###child
                    child_chart[i].clear()

                    child_chart[i].get_xaxis().set_visible(False)
                    child_chart[i].get_yaxis().set_visible(False)
                    child_chart[i].imshow(self.temperature_upscale, cmap='jet', vmin=min_temp, vmax=max_temp)

                    child_canvas[i].draw()
                    # print("worker{num} 작동중".format(num = i))
                    # print(canvas[i])
                    # time.sleep(0.1)
            except:
                print("drawing fail : ", self.cam_num)



###worker1
worker = Worker()
worker.moveToThread(thread)
thread.started.connect(worker.get_temperature)


###worker2
worker_draw_canvas = Worker2(camera_num= camera_num)
worker_draw_canvas.moveToThread(thread_draw_chart)
thread_draw_chart.started.connect(worker_draw_canvas.display_plot)

thread.start()
thread_draw_chart.start()


# app.exec_() ## 확인

# ClientSocket.close()
