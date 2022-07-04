import time
import keyboard
import win32api, win32con
import sys
from PIL import Image
import numpy
import pyautogui

def unclick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

def move_at_screen(x: int, y: int):
    win32api.SetCursorPos((x, y))

def move_at_canvas(x: int, y: int, offset: tuple):
    win32api.SetCursorPos((x + offset[0], y + offset[1]))

def wait():
    time.sleep(0.025)

def unglitch(res: tuple, offset: tuple):
    freq = 24
    for y in range(res[1]):
        if keyboard.is_pressed('q'):
            sys.exit()
        if y % freq != 0:
            continue
        for x in range(res[0]):
            if x % freq != 0:
                continue
            move_at_canvas(x, y, offset)
            time.sleep(0.0001)


while not keyboard.is_pressed('p'):
    wait()
while keyboard.is_pressed('p'):
    wait()

video_resolution = (960, 720)
canvas_position = (24, 163)
black_position = (762, 62)
white_position = (762, 83)

move_at_screen(black_position[0], black_position[1])
click()
wait()
unclick()

# start = time.time()
# unglitch(video_resolution, canvas_position)
# print(time.time() - start)
# sys.exit()

start_frame = 456
frame_counter = start_frame-4
color = 'black'
color_is_black = True
running = True
last_frame_time = time.time()
while running:
    img = Image.open(f'./frame-sequence/{frame_counter:04}.png')
    frame = numpy.asarray(img)
    
    # Go through each pixel and draw it
    paused = False
    freq = 8
    for y in range(len(frame)):
        if y % freq == 0:
            for x in range(len(frame[y])):
                if x % freq == 0:
                    if keyboard.is_pressed('p'):
                        position = pyautogui.position()
                        unclick()
                        print(f'paused on y={y} x={x} black={color_is_black} position={position}')
                        while keyboard.is_pressed('p'):
                            if keyboard.is_pressed('q'):
                                running = False
                                print('exiting')
                                break
                        while not keyboard.is_pressed('p'):
                            if keyboard.is_pressed('q'):
                                running = False
                                print('exiting')
                                break
                        while keyboard.is_pressed('p'):
                            if keyboard.is_pressed('q'):
                                running = False
                                print('exiting')
                                break
                        if running:
                            move_at_screen(position[0], position[1])
                            wait()
                            click()
                        else:
                            break
                    if keyboard.is_pressed('q'):
                        unclick()
                        running = False
                        print('exiting')
                        break
                    if x != 0:
                        if (frame[y][x][0] < 128) != color_is_black:
                            # print(f'new color!!!! {x}, r={frame[y][x][0] < 128}, black={color_is_black}')
                            move_at_canvas(x, y, canvas_position)
                            wait()
                            unclick()
                            wait()
                            if color_is_black:
                                move_at_screen(white_position[0], white_position[1])
                                wait()
                                click()
                                wait()
                                color_is_black = False
                            else:
                                move_at_screen(black_position[0], black_position[1])
                                wait()
                                click()
                                wait()
                                color_is_black = True
                            unclick()
                            move_at_canvas(x, y, canvas_position)
                            wait()
                            click()
                            # wait()
                    else:
                        if frame[y][x][0] >= 128:
                            if color_is_black:
                                move_at_screen(white_position[0], white_position[1])
                                wait()
                                click()
                                wait()
                            color_is_black = False
                        elif frame[y][x][0] < 128:
                            if not color_is_black:
                                move_at_screen(black_position[0], black_position[1])
                                wait()
                                click()
                                wait()
                            color_is_black = True
                        unclick()
                        move_at_canvas(x, y, canvas_position)
                        click()
                        wait()
            move_at_canvas(len(frame[y]) - 1, y, canvas_position)
            unclick()
        if not running:
            break
    unglitch(video_resolution, canvas_position)
    wait()
    if frame_counter >= start_frame:
        screenshot = pyautogui.screenshot()
        screenshot.save(f'render-frames/{frame_counter:04}.png')
    print(f'Finished frame {frame_counter:04} in {time.time() - last_frame_time} seconds.')
    frame_counter += 1
    last_frame_time = time.time()
print(f'quit on y={y} x={x} black={color_is_black} position={position} frame={frame_counter}')
print('press m to close')
while not keyboard.is_pressed('m'):
    pass