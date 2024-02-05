"""
Records screen and saves it as '.avi' file
"""


import cv2
import numpy as np
import pyautogui
from datetime import datetime
import os


PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # recordings go here
RESOLUTION = (1920, 1080)
FRAMES = 20.0

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
file_name = f'{datetime.now().strftime("%y%m%d-%H%M%S")}_screen_recording.avi'
file_path = os.path.join(PATH, file_name)
out = cv2.VideoWriter(file_path, fourcc, FRAMES, RESOLUTION)

# Start the screen recording
recording = True

while recording:
    img = pyautogui.screenshot(region=(0, 0, pyautogui.size()[0], pyautogui.size()[1]))  # capture screen image
    frame = np.array(img)  # convert to array
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert color space from BGR to RGB
    out.write(frame)  # write frame to video file
    cv2.imshow('Screen Recorder', frame)  # display resulting frame

    if cv2.waitKey(1) == 27:   # check for 'Esc' key press
        recording = False

out.release()  # release video writer
cv2.destroyAllWindows()  # close windows
