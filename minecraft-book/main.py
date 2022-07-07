import time
import keyboard
import win32api, win32con
import sys
from math import floor
from PIL import Image
import numpy
import pyautogui

def press_and_release(key: str):
    keyboard.press(key)
    time.sleep(0.01)
    keyboard.release(key)

def click(pos: tuple):
    win32api.SetCursorPos(pos)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def move_pages(num: int, pos: tuple):
    if num <= 0: return
    for i in range(num):
        click(pos)

video_resolution = (960, 720)
output_resolution = (19, 10)
book_resolution = (19, 14)

next_position = (1060, 500)
search_position = (1210, 290)
quill_position = (715, 400)
empty_position = (715, 460)
slot_1_position = (715, 680)

while not keyboard.is_pressed('p'):
    time.sleep(0.01)
while keyboard.is_pressed('p'):
    time.sleep(0.01)

press_and_release('backspace')

frame_counter = 1
page_number = frame_counter % 100
move_pages(page_number - 1, next_position)
last_frame_time = time.time()
running = True
while running:
    img = Image.open(f'./frame-sequence/{frame_counter:04}.png')
    frame = numpy.asarray(img)

    freq = (video_resolution[0] / output_resolution[0], video_resolution[1] / output_resolution[1])
    for y in range(len(frame)):
        if floor(y % freq[1]) != 0:
            continue
        to_type = ''
        for x in range(len(frame[y])):
            if floor(x % freq[0]) != 0:
                continue
            to_type += ' ' if frame[y][x][0] >= 128 else '#'
            if keyboard.is_pressed('q'):
                running = False
                sys.exit()
        keyboard.write(to_type)
        press_and_release('return')

    screenshot = pyautogui.screenshot()
    screenshot.save(f'render-frames/{frame_counter:04}.png')

    # for y in range(len(frame)):
    #     if floor(y % freq[1]) != 0:
    #         continue
    #     for x in range(len(frame[y])):
    #         if floor(x % freq[0]) != 0:
    #             continue
    #         press_and_release('backspace')
    #         if keyboard.is_pressed('q'):
    #             running = False
    #             sys.exit()
    #     press_and_release('backspace')

    if frame_counter % 100 == 0:
        sleep_time = 0.2
        # Get new book
        press_and_release('escape')
        time.sleep(sleep_time)
        press_and_release('e')
        time.sleep(sleep_time)
        click(search_position)
        time.sleep(sleep_time)
        keyboard.write('quill')
        time.sleep(sleep_time)
        click(quill_position)
        time.sleep(sleep_time)
        click(slot_1_position)
        time.sleep(sleep_time)
        click(empty_position)
        time.sleep(sleep_time)
        press_and_release('escape')
        time.sleep(sleep_time)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
        time.sleep(sleep_time)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
        win32api.SetCursorPos(next_position)
        time.sleep(sleep_time)
    else:
        move_pages(1, next_position)
    
    if keyboard.is_pressed('q'):
        running = False
        sys.exit()
    
    
    print(f'Finished frame {frame_counter:04} in {time.time() - last_frame_time} seconds.')
    frame_counter += 1
    last_frame_time = time.time()