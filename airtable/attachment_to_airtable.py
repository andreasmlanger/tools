"""
Adds files from a Windows Explorer folder to an Airtable table as attachments
The Airtable website needs to be opened on the left side of the screen, Windows Explorer on the right
The first file needs to be selected in Details view, the cursor on the website needs to be in the first title field
Start the script, then open the website window, then the Windows Explorer
"""


import pyautogui
import pyperclip
from datetime import datetime
import time


# COLUMN = 'Map'
COLUMN = 'Images'


class Upload:
    def __init__(self):
        self.file_name = None
        time.sleep(5)  # initialization time
    
    @staticmethod
    def get_filename_from_explorer():
        time.sleep(0.5)
        pyautogui.press('f2')
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.press('enter')
        return pyperclip.paste()
    
    def add_attachments(self):
        while True:
            # Get filename from Windows Explorer
            file_name = self.get_filename_from_explorer()
            if file_name == self.file_name:
                break
            else:
                self.file_name = file_name
            date_of_file = datetime.strptime(file_name[:6], "%y%m%d")
            
            # Switch to Airtable website and find matching date
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'left')
            time.sleep(0.5)
            pyautogui.press('right')
            while True:
                pyautogui.hotkey('ctrl', 'c')
                date_of_airtable_record = datetime.strptime(pyperclip.paste(), "%Y-%m-%d")
                if date_of_airtable_record != date_of_file:
                    pyautogui.press('down')  # try next row
                else:
                    break
            pyautogui.hotkey('ctrl', 'right')
            if COLUMN == 'Images':
                pyautogui.press('left')
            pyautogui.press('enter')  # open upload screen

            # Drag file onto Airtable upload
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.5)
            screen_w, screen_h = pyautogui.size()
            (x, y, _, _) = pyautogui.locateOnScreen('data/blue.png', region=(0, 300, screen_w, screen_h))
            pyautogui.mouseDown(x + 10, y + 10, button='left')
            pyautogui.moveTo(500, screen_h // 2, duration=0.3)
            pyautogui.mouseUp(500, screen_h // 2, button='left')
            time.sleep(0.5)
            pyautogui.click(150, 550)
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('enter')  # upload button
            time.sleep(4)
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.5)
            pyautogui.press('down')  # next file


def main():
    Upload().add_attachments()


if __name__ == '__main__':
    main()
