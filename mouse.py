# sample program to automate the mouse movement along with the clicks

import pyautogui
import time

pyautogui.position()

for i in range(1,10000):
    time.sleep(5)
    pyautogui.moveTo(400,550)
    pyautogui.click()
    time.sleep(5)
    pyautogui.moveTo(1811,955)
    pyautogui.click()

# Basics of screen Bots to keep the cursor busy