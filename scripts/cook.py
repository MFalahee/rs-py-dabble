import pyautogui
import random
import numpy as np
import tkinter as tk
import time
from mousepath import wind_mouse

scr_width, scr_height = pyautogui.size()
current_x, current_y = pyautogui.position()
fire_x_range = (160, 220)
fire_y_range = (475, 515)
bank_x_range = (355, 450)
bank_y_range = (285, 540)
deposit_x_range = (460, 490)
deposit_y_range = (390, 420)
food_x_range = (445, 465)
food_y_range = (115, 135)
root = tk.Tk()
root.attributes('-topmost', True)
root.geometry("300x200+0+0")
root.title("Cooking")
root.anchor = "nw"

def random_coords(x_range, y_range):
    return random.randint(x_range[0], x_range[1]), random.randint(y_range[0], y_range[1])

def location_scaled_to_window(x, y, corner):
    return x + corner[0], y + corner[1]

def cook(left_corner, mouse_move):
    # make sure window is active
    total = pyautogui.prompt(text="Enter the number of food you want cooked", title="Cooking", default="0")
    inventories = np.ceil(int(total) / 28)
    print("Cooking " + total + " food in " + str(inventories) + " inventories")
    # do x amount of times
    for i in range (0, int(inventories)):
        print("Starting inventory " + str(i + 1) + " of " + str(inventories))
        target = random_coords(fire_x_range, fire_y_range)
        target = location_scaled_to_window(*target, left_corner)
        wind_mouse(*pyautogui.position(), *target, move_mouse=mouse_move) # move mouse to fire
        time.sleep((random.random() / 10 ) + 0.02)
        pyautogui.click() # click fire
        time.sleep((random.random() / 5) + 0.5)
        pyautogui.press('space')  # start cooking
        time.sleep((random.random() / 5) + 1.5)
        target = random_coords(bank_x_range, bank_y_range)
        target = location_scaled_to_window(*target, left_corner)
        wind_mouse(*pyautogui.position(), *target, move_mouse=mouse_move) # move mouse to bank npc
        time.sleep((random.random() / 10) + random.randint(65,75))
        # sleep until done cooking (and add random time to simulate human error)
        print("Banking!")
       
        time.sleep((random.random() / 10) + 0.2)
        pyautogui.click()
        time.sleep((random.random() / 5) + 0.2)
        target = random_coords(deposit_x_range, deposit_y_range)
        target = location_scaled_to_window(*target, left_corner)
        wind_mouse(*pyautogui.position(), *target, move_mouse=mouse_move) # move mouse to deposit button
        time.sleep((random.random() / 5) + 0.2)
        pyautogui.click()
        time.sleep((random.random() / 5) + 0.2)
        target = random_coords(food_x_range, food_y_range)
        target = location_scaled_to_window(*target, left_corner)
        wind_mouse(*pyautogui.position(), *target, move_mouse=mouse_move) # move mouse to food slot
        time.sleep((random.random() / 5) + 0.2)
        pyautogui.click()
        time.sleep((random.random() / 5) + 0.2)
        # done at rogues den fully zoomed in standing on south tile from fire
    print("Done cooking!")


root.destroy()