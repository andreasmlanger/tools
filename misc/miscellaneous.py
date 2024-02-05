"""
Miscellaneous helper functions
"""

import pyautogui
import time


def print_colors():
    """
    Prints different colors in Python console
    """
    for i in list(range(30, 39)) + list(range(90, 98)):
        print('\033[' + str(i) + 'm' + str(i))


def print_cursor_position():
    """
    Prints coordinates of cursor on screen
    """
    while True:
        time.sleep(2)
        print(pyautogui.position())


print_colors()
# print_cursor_position()
