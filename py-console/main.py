import cv2
import time
import keyboard
from math import floor
import os

cap = cv2.VideoCapture('bad-apple.mp4')
fps = 30

og_resolution = (690, 720)
new_resolution = (76, 29)
console_resolution = (119, 29)
blank_before = int((console_resolution[0] - new_resolution[0]) / 2.0)
frequency = (og_resolution[0] / new_resolution[0], og_resolution[1] / new_resolution[1])
clear = lambda: os.system('cls')

os.system('')
new_frame_escape = f'\033[{new_resolution[0] + blank_before}D\033[{new_resolution[1]}A'
new_line_escape = f'\033[{new_resolution[0] + blank_before}D\033[1B'

if not cap.isOpened():
    print('ERROR: VIDEO NOT OPENED')

frame_counter = 0
start_time = time.time()
while cap.isOpened():
    ret, frame = cap.read()

    # Check if we should stop, and stop
    if ret == True:
        if keyboard.is_pressed('q'):
            break
    else:
        break

    # Convert the big frame into a grid of pixels that can fit on the terminal 
    terminal_grid = []
    for y in range(len(frame)):
        if floor(y % frequency[1]) == 0:
            row = []
            for x in range(len(frame[y])):
                if floor(x % frequency[0]) == 0:
                    row.append(frame[y][x][0] >= 128)
            terminal_grid.append(row)

    # Draw in terminal
    to_print = ''
    for y in range(new_resolution[1]):
        for i in range(blank_before):
            to_print += ' '
        for x in range(new_resolution[0]):
            to_print += '#' if terminal_grid[y][x] else ' '
        to_print += new_line_escape
    to_print += new_frame_escape
    print(to_print)
    
    # Wait until the next frame should be displayed - we don't want to be running a 30 fps at 70 fps now do we?
    frame_counter += 1
    while time.time() - start_time < frame_counter * (1 / fps):
        pass
cap.release()
cv2.destroyAllWindows()