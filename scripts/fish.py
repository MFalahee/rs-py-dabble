import pyautogui
import random
import numpy as np
import tkinter as tk
import time
from PyQt5 import QtCore, QtGui
from mousepath import wind_mouse
import cv2
import os

scr_width, scr_height = pyautogui.size()
current_x, current_y = pyautogui.position()
root = tk.Tk()
root.attributes('-topmost', True)
root.geometry("300x200+0+0")
root.title("Fishing")
root.anchor = "nw"

compass_x_range = (625, 645)
compass_y_range =(35, 50)
fishing_overlay_x_range = (45, 100)
fishing_overlay_y_range = (50, 75)
first_look_x_range = (400, 500)
first_look_y_range = (275, 360)
second_look_x_range = (400, 500)
second_look_y_range = (200, 500)


def random_coords(x_range, y_range):
    return random.randint(x_range[0], x_range[1]), random.randint(y_range[0], y_range[1])
def location_scaled_to_window(x, y, corner):
    return x + corner[0], y + corner[1]
def search_for_images(region=None):
    image_dir = os.path.join(os.path.dirname(__file__), '..', 'images', 'fishing')
    # List all files in the directory
    image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    # Iterate through each image and try to find it on the screen
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        location = pyautogui.locateOnScreen(image_path, confidence=0.9, region=region)
        if location:
            return location
    return None
    # Return results
def are_we_fishing(self):
    #  check for fishing overlay
    loc1 = location_scaled_to_window(fishing_overlay_x_range[0], fishing_overlay_y_range[0], self.left_corner)
    loc2 = location_scaled_to_window(fishing_overlay_x_range[1], fishing_overlay_y_range[1], self.left_corner)
    found = pyautogui.locateOnScreen('images/fishing.png', region=(loc1[0], loc1[1], loc2[0] - loc1[0], loc2[1] - loc1[1]), confidence=0.9)
    if found:
         return True
    return False

def setup_inventory(self):
    inventory_x_range = (615,776)
    inventory_y_range = (264, 511)
    spacing = 5
    num_rect_x = 4
    num_rect_y = 7
    inventory_squares = []
    rect_width = (inventory_x_range[1] - inventory_x_range[0] - (num_rect_x - 1) * spacing) / num_rect_x
    rect_height = (inventory_y_range[1] - inventory_y_range[0] - (num_rect_y - 1) * spacing) / num_rect_y
    for i in range(num_rect_x):
        for j in range(num_rect_y):
            # scale to window prior to adding to list
            scaled = location_scaled_to_window(int(inventory_x_range[0] + i * (rect_width + spacing)), int(inventory_y_range[0] + j * (rect_height + spacing)), self.left_corner)
            inventory_squares.append(scaled)
    return inventory_squares
def drop_inventory(self, inventory_squares):
    # drop inventory spots with fish
    # 4x7 inventory defined above
    # inventory[0] is top left
    # inventory[27] is bottom right
    # keep first 6 spots for feathers, rod, pestle and mortar, knife, and herb
    # drop the rest
    for i in range(6, len(inventory_squares)):
        print("Dropping item " + str(i))
        target = random_coords((inventory_squares[i][0], inventory_squares[i][0] + 10), (inventory_squares[i][1], inventory_squares[i][1] + 10))
        wind_mouse(*pyautogui.position(), *target, move_mouse=self.move_mouse)
        time.sleep((random.random() / 10 ) + 0.02)
        pyautogui.click()
        time.sleep((random.random() / 10 ) + 0.02)

def start(self):
    # make sure window is active
    # check if 3ticking or not
    # check if inventory is full
    # move mouse to compass, and click to rotate camera north
    # assume last three inventory spots are offlimits (feathers, rod, pestle and mortar)
    # look for first fishing spot
    target = random_coords(compass_x_range, compass_y_range)
    target = location_scaled_to_window(*target, self.left_corner)
    wind_mouse(*pyautogui.position(), *target, move_mouse=self.move_mouse) # move mouse to compass
    time.sleep((random.random() / 10 ) + 0.02)
    pyautogui.click()
    time.sleep((random.random() / 10 ) + 0.02)

    # look for first fishing spot
    scaled_first_region = [self.left_corner[0] + first_look_x_range[0], self.left_corner[1] + first_look_y_range[0], first_look_x_range[1] - first_look_x_range[0], first_look_y_range[1] - first_look_y_range[0]]
    scaled_second_region = [self.left_corner[0] + second_look_x_range[0], self.left_corner[1] + second_look_y_range[0], second_look_x_range[1] - second_look_x_range[0], second_look_y_range[1] - second_look_y_range[0]]
    location = search_for_images(region=scaled_first_region)
    if location:
            print(f"Image found at: {location}")
            target = random_coords((location[0], location[0] + location[2]), (location[1], location[1] + location[3] - 10))
            wind_mouse(*pyautogui.position(), *target, move_mouse=self.move_mouse)
            time.sleep((random.random() / 10 ) + 0.02)
    
    location = search_for_images(region=scaled_second_region)
    if location:
            print(f"Image found at: {location}")
            target = random_coords((location[0], location[0] + location[2] - 5), (location[1], location[1] + location[3] - 5))
            wind_mouse(*pyautogui.position(), *target, move_mouse=self.move_mouse)
    else:
        print("None of the images were found on the screen.")
    inventory = setup_inventory(self)
    if (pyautogui.locateOnScreen('images/fishinginventfull.png', confidence=.9) != None):
        print("Inventory is full")
        drop_inventory(self, inventory)