import pyautogui
import random
import numpy as np
import tkinter as tk
import time
from PyQt5 import QtCore, QtGui
from mousepath import wind_mouse

scr_width, scr_height = pyautogui.size()
current_x, current_y = pyautogui.position()
root = tk.Tk()
root.attributes('-topmost', True)
root.geometry("300x200+0+0")
root.title("Fishing")
root.anchor = "nw"

compass_x_range = (625, 645)
compass_y_range =(35, 50)
inventory_x_range = (600,785)
inventory_y_range = (255, 515)
interact_x_range = ()
interact_y_range = ()


def random_coords(x_range, y_range):
    return random.randint(x_range[0], x_range[1]), random.randint(y_range[0], y_range[1])

def location_scaled_to_window(x, y, corner):
    return x + corner[0], y + corner[1]

def paint():
        painter = QtGui.QPainter(self)
        if self.mode == "idle":
            painter.setPen(QtCore.Qt.green)
        else:
            painter.setPen(QtCore.Qt.red)
        painter.drawLine(0,0,0,self.current_size[1])
        painter.drawLine(0,0,self.current_size[0],0)
        painter.drawLine(self.current_size[0],0,self.current_size[0],self.current_size[1])
        painter.drawLine(0,self.current_size[1],self.current_size[0],self.current_size[1])

def setup(left_corner, mouse_move):
    # make sure window is active
    # draw paint using Qt around inventory, compass, and interact
    # move mouse to compass, and click to rotate camera north
    



    target = random_coords(compass_x_range, compass_y_range)

def fish(left_corner, mouse_move):
