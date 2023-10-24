import json
import pyautogui
import time
from mousepath import wind_mouse
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui
import win32gui
import win32api
import win32con
import win32com.client
from pynput import mouse, keyboard
from scripts import cook

global hwnd
DEBUG = False
START_TIME = time.time()
RIGHT_CLICK = 0
LEFT_CLICK = 1
EXTRA_SLEEP = 0.5
SAVE_DIR = '/saves/'

pyautogui.FAILSAFE = False

x_size = win32api.GetSystemMetrics(0)
y_size = win32api.GetSystemMetrics(1)
shell = win32com.client.Dispatch("WScript.Shell")
class runeliteWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()

        # configuration
        self.config = config
        self.mode = "idle"

        # Screen setup
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint | 
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.current_size = self.config['window_size']
        self.left_corner = self.config['left_corner']
        self.move(*self.left_corner)
        self.right_corner = (self.left_corner[0] + self.current_size[0], self.left_corner[1] + self.current_size[1])
        self.setMinimumSize(QtCore.QSize(self.current_size[0] + 1, self.current_size[1] + 1))
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        keyboard_listener.start()
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()
        # threading.Thread(target=self.background_thread, daemon=True).start()
        # find_window_then_resize_and_move(self.config['window_name'], self.left_corner, self.current_size)
        # time.sleep(0.5)
    def on_click(self, x, y, button, pressed):
        if DEBUG: 
            print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
    def on_press(self, key):
        if DEBUG: 
            try:
                print('alphanumeric key {0} pressed'.format(key.char))
            except AttributeError:
                print('special key {0} pressed'.format(key))
    def on_release(self, key):
        try: 
            key = '{0}'.format(key.char)
        except AttributeError:
            key = '{0}'.format(key)
            key = key.split('.')[1]
        if DEBUG:
            print(key, "released")
        if key == self.config["close"]:
            print("Closing")
            QApplication.quit()
            return False
        elif key == self.config["idle"]:
            self.mode = "idle"
        elif key == self.config["cook"]:
            self.mode = "cook"
            cook.cook(self.left_corner, self.move_mouse)
        self.update()

    def move_mouse(self, x, y, box_movement = True):
        if box_movement:
            x_dest, y_dest = self.box_movement(x, y)
        else:
            x_dest, y_dest = x, y
        x_conv = int(65535 * x_dest / x_size)
        y_conv = int(65535 * y_dest / y_size)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, x_conv, y_conv)

    # Prevents predicted mouse movements from going outside the application area
    def box_movement(self, x, y):
        new_x = min(max(self.left_corner[0], x), self.right_corner[0])
        new_y = min(max(self.left_corner[1], y), self.right_corner[1])
        return (new_x, new_y)
    def in_window(self, x, y):
        if x < self.left_corner[0] or x > self.right_corner[0]:
            return False
        if y < self.left_corner[1] or y > self.right_corner[1]:
            return False
        return True
    
    def full_to_window(self, position):
        p0 = min(max(position[0] - self.left_corner[0], 0), self.current_size[0] - 1)
        p1 = min(max(position[1] - self.left_corner[1], 0), self.current_size[1] - 1)
        return (p0, p1)

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        if self.mode == "idle":
            painter.setPen(QtCore.Qt.green)
        else:
            painter.setPen(QtCore.Qt.red)
        painter.drawLine(0,0,0,self.current_size[1])
        painter.drawLine(0,0,self.current_size[0],0)
        painter.drawLine(self.current_size[0],0,self.current_size[0],self.current_size[1])
        painter.drawLine(0,self.current_size[1],self.current_size[0],self.current_size[1])
def find_window_then_resize_and_move(window_name, position, size): 
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        print("Window not found.", window_name)
        return None
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, *position, *size, win32con.SWP_SHOWWINDOW)
    print ("Window", window_name, "found and resized.")
iflag = False

if __name__ == "__main__":
    config_file = open('config.txt', 'r')
    config = json.loads(config_file.read())
    app = QApplication([config])
    mainWin = runeliteWindow(config)
    mainWin.show()
    find_window_then_resize_and_move(config['window_name'], mainWin.left_corner, mainWin.current_size)
    app.exec_() 
    print('done')
