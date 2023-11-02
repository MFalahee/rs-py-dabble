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
        self.start_time = time.time()
        self.last_click = time.time()
        self.region = self.location_scaled_to_window(610, 640, 110, 140)
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
        elif key == "w":
            self.mode = "idle"
        elif key == "esc":
            self.mode = "done"
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
                print(image_file)
                return location
        return None

    def flick(self):
        max_loops = 100
        loops = 0
        pyautogui.click()
        self.last_click = self.start_time
        time_passed = 0
        while self.mode != "done":
            time_passed += (time.time() - self.start_time)
            loops += 1
            if self.mode == "idle":
                loops = 0
                time.sleep(0.05)
            if loops >= max_loops:
                self.mode = "idle"
                break
            if loops % 5 == 0:
                print("Loop: " + str(loops))
                # print("Running for: " + str(round(self.start_time, 2)) + " seconds" + "|||||| + Last click: " + str(round(self.last_click, 2)) + " seconds ago")
            toggleSpots = self.search_for_images(self.region)
            if (toggleSpots != None or self.last_click > 0.7) and self.mode == "flick":
                print(toggleSpots, self.last_click)
                time.sleep((random.random() / 100) + 0.03)
                pyautogui.click()
                time.sleep((random.random() / 100) + 0.43)
                pyautogui.click()
                self.last_click = time.time() - self.last_click
            else:
                time.sleep(0.05)
                continue