import time
import keyboard
import win32api, win32con
import sys
from PIL import Image
import numpy
import pyautogui

def click_screen(x: int, y: int):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def click_screen(pos: tuple):
    win32api.SetCursorPos(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

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
    # Go through every 24 pixels to try and move the mouse everywhere to unglitch Paint
    freq = 20
    for y in range(res[1]):
        if keyboard.is_pressed('q'):
            running = False
            print('exiting')
            break
        if y % freq != 0:
            continue
        for x in range(res[0]):
            if x % freq != 0:
                continue
            move_at_canvas(x, y, offset)
            time.sleep(0.0001)
        move_at_canvas(res[0] - 1, y, offset)
        time.sleep(0.0001)

def change_color(is_white: bool):
    if is_white:
        move_at_screen(white_position[0], white_position[1])
    else:
        move_at_screen(black_position[0], black_position[1])
    wait()
    click()
    wait()
    unclick()

# Wait until P is pressed and un-pressed for the user to switch to Paint before starting.
while not keyboard.is_pressed('p'):
    wait()
while keyboard.is_pressed('p'):
    wait()

# Set variables about the video and Paint
video_resolution = (960, 720)
canvas_position = (24, 163)
black_position = (762, 62)
white_position = (762, 83)
brush_position_1 = (330, 98)
brush_position_2 = (330, 137)
size_position_1 = (638, 67)
size_position_2 = (667, 255)

# Make sure Paint is setup
click_screen(brush_position_1)
time.sleep(1) # More waiting to allow for the menu to come up
click_screen(brush_position_2)
wait()
click_screen(size_position_1)
time.sleep(1) # More waiting to allow for the menu to come up
click_screen(size_position_2)
wait()
click_screen(black_position)
wait()
# Set starting variables
start_frame = 1724 # To know when to start saving frames (due to antialiasing making stuff weird)
frame_counter = start_frame-4 # Frame counter to know what frame to render
color_is_black = True # Starting color
running = True # Loop variable
last_frame_time = time.time() # To get frame time (generally around a minute)
while running:
    img = Image.open(f'./frame-sequence/{frame_counter:04}.png')
    frame = numpy.asarray(img)
    
    # Go through each row and draw it
    freq = 8
    for y in range(len(frame)):
        if y % freq == 0:
            # Go through each pixel in the row, check if the color is different from the section we're in.
            # If it is different, move the cursor and unclick, change colors, and click again.
            for x in range(len(frame[y])):
                if x % freq == 0:
                    # Check for pause
                    if keyboard.is_pressed('p'):
                        # Wait for p to stop being pressed, then wait for it to be pressed again (while also checking for quits)
                        position = pyautogui.position()
                        unclick()
                        print(f'paused on y={y} x={x} black={color_is_black} position={position} frame={frame_counter}')
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
                    # Check for quits
                    if keyboard.is_pressed('q'):
                        unclick()
                        running = False
                        print('exiting')
                        break
                    if x != 0:
                        # Check if the current color is different from the color of the row we're on
                        if (frame[y][x][0] < 128) != color_is_black:
                            # Move cursor to draw line and unclick
                            move_at_canvas(x, y, canvas_position)
                            wait()
                            unclick()
                            wait()
                            # Swap colors
                            change_color(color_is_black)
                            color_is_black = not color_is_black
                            # Move cursor back and start drawing a new line
                            move_at_canvas(x, y, canvas_position)
                            wait()
                            click()
                    else:
                        # Check the color of the frame, check the current color, and change if needed
                        if (frame[y][x][0] < 128) != color_is_black:
                            change_color(color_is_black)
                            color_is_black = not color_is_black
                        # Start new row
                        move_at_canvas(x, y, canvas_position)
                        click()
                        wait()
            move_at_canvas(len(frame[y]) - 1, y, canvas_position)
            unclick()
            wait()
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