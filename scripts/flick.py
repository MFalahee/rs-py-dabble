import pyautogui
import random
import time
import os
from pynput import keyboard

DEBUG = False



class TickFlick():
    def __init__(self, corner):
        self.mode = 'flick'
        self.corner = corner
        self.start = time.time()
        self.region = self.location_scaled_to_window(600, 640, 110, 140)
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()
  
    def location_scaled_to_window(self, x1, x2, y1, y2):
        return (int(x1 + self.corner[0]), int(y1 + self.corner[1]), int(x2 + self.corner[0]),int(y2 + self.corner[1]))

    def on_release(self, key):
        try: 
            key = '{0}'.format(key.char)
        except AttributeError:
            key = '{0}'.format(key)
            key = key.split('.')[1]
        if key == "q":
            self.mode = "flick"
        else:
            self.mode = "idle"

    def on_press(self, key):
        if DEBUG: 
            try:
                print('alphanumeric key {0} pressed'.format(key.char))
            except AttributeError:
                print('special key {0} pressed'.format(key))
    def search_for_images(self, region):
        image_dir = os.path.join(os.path.dirname(__file__), '..', 'images', 'flick')
        # List all files in the directory
        image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
        # Iterate through each image and try to find it on the screen
        for image_file in image_files:
            image_path = os.path.join(image_dir, image_file)
            location = pyautogui.locateOnScreen(image_path, confidence=0.9, region=region)
            if location:
                return location
        return None

    def flick(self):
        start_time = time.time()
        max_loops = 1000
        loops = 0
        pyautogui.click()
        running_time = start_time
        last_click = 0
        while self.mode == "flick":
            running_time = time.time() - running_time
            loops += 1
            if loops % 5 == 0:
                print("Loop: " + str(loops))
                print("Running for: " + str(round(running_time, 2)) + " seconds" + "|||||| + Last click: " + str(round(last_click, 2)) + " seconds ago")
            cycle = self.search_for_images(self.region)
            if loops >= max_loops:
                self.mode = "idle"
                break
            if cycle != None:
                time.sleep((random.random() / 100 ) + 0.02)
                pyautogui.click()
                last_click = time.time() - start_time
            else:
                if last_click >= 0.7:
                    pyautogui.click()
                    last_click = time.time() - start_time
                time.sleep(0.05)