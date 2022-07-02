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

if not cap.isOpened():
    print('ERROR: VIDEO NOT OPENED')

frame_counter = 0
start_time = time.time()
last_frame_time = time.time()
lowest_fps = 1000
highest_fps = 0
while cap.isOpened():
    ret, frame = cap.read()
    og_resolution = (len(frame), len(frame[0]))
    ratio = og_resolution[0] / og_resolution[1]
    new_resolution = (max(0, min(console_resolution[0], (round(2.73 * ratio * 29)))), 29)
    frequency = (og_resolution[0] / new_resolution[0], og_resolution[1] / new_resolution[1])
    frame_bw = frame
    terminal_board = []
    for y in range(len(frame)):
        if floor(y % frequency[1]) == 0:
            row = []
            for x in range(len(frame[y])):
                if floor(x % frequency[0]) == 0:
                    frame_bw[y][x] = [255, 255, 255] if frame_bw[y][x][0] >= 128 else [0, 0, 0]
                    row.append(frame_bw[y][x][0] == 255)
            terminal_board.append(row)
    clear()
    print(f'size (tuple): {new_resolution[0]}x{new_resolution[1]}')
    print(f'size (actual): {len(terminal_board[0])}x{len(terminal_board)}')

    for y in range(new_resolution[1]):
        for i in range(blank_before):
            print(' ', end='')
        for x in range(new_resolution[0]):
            end = '\n' if x == new_resolution[0] - 1 else ''
            ascii_char = '#' if terminal_board[y][x] else ' '
            print(ascii_char, end=end)

    if ret == True:
        # cv2.imshow('Bad Apple', frame_bw)
        if keyboard.is_pressed('q'):
            break
    else:
        break

    frame_counter += 1
    fps = 1/(time.time() - last_frame_time)
    if frame_counter > 5:
        highest_fps = fps if fps > highest_fps else highest_fps
        lowest_fps = fps if fps < lowest_fps else lowest_fps
    # print(f'FPS BITCH: {fps}')
    print(f'lowest: {lowest_fps}, highest: {highest_fps}')
    time.sleep(0.06)
    last_frame_time = time.time()
cap.release()
cv2.destroyAllWindows()