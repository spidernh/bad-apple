import time
import keyboard
import win32api, win32con
import sys
from PIL import Image
import numpy
import pyautogui
import datetime

# frame = 1
# print(f'render-frames\\{frame:04}.png')
# 
# img = Image.open('frame-sequence/0310.png')
# print(type(img))
# # img.show()
# print(img.format)
# frame = np.asarray(img)
# print(type(frame))
# print(str(frame))

# def change_color(color):
#     print(f'Changing color to {"white" if color else "black"}')
    

# color_is_black = True
# new_color = 255
# if (new_color < 128) != color_is_black:
#     change_color(color_is_black)
#     color_is_black = not color_is_black

# if new_color >= 128:
#         if color_is_black:
#             change_color(True)
#         color_is_black = False
# elif new_color < 128:
#     if not color_is_black:
#         change_color(False)
#     color_is_black = True

# print(f'color: {"black" if color_is_black else "white"}')

# last_frame = 1
# frame_counter = last_frame
# A test I made to automatically switch to different sections I needed to redo due to:
#    Not unglitching
#    Taskbar not the same as other frames
#    Entered in 5533 instead of 5433 so I skipped 100 frames
#    The last frames (not redone, they just needed to be done)
last_frame = 1
frame_counter = 1
last_frame_time = time.time()
section = 0

while not keyboard.is_pressed('q'):
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    delta_time = round(time.time() - last_frame_time, 2)
    if frame_counter >= last_frame:
        # screenshot = pyautogui.screenshot()
        # screenshot.save(f'render-frames/{frame_counter:04}.png')
        pass
    if frame_counter == 6572 and section == 3:
        message = f'Finished frame 6572 in {delta_time} seconds, Bad Apple!! is done at {current_time} !!!!!!!!'
        print(message)
        f = open('end_time.txt', 'w')
        f.write(message)
        f.close()
        while not keyboard.is_pressed('q'):
            pass
        sys.exit()
    else:
        print(f'Finished frame {frame_counter:04} in {delta_time} seconds at {current_time}, screenshot={frame_counter >= last_frame}.')
    if frame_counter > 457 and section == 0:
        # Finished first section, (no unglitch) transition to second section
        last_frame = 1882
        frame_counter = last_frame - 5
        section = 1
        print(f'Ready to start on frame {frame_counter} to render {last_frame} and beyond.')
    elif frame_counter > 1917 and section == 1:
        # Finished second section (taskbar issue), transition to third section
        last_frame = 5452
        frame_counter = last_frame - 5
        section = 2
        print(f'Ready to start on frame {frame_counter} to render {last_frame} and beyond.')
    elif frame_counter > 5553 and section == 2:
        # Finished third section (mistyped first frame), transition to fourth section
        last_frame = 6228
        frame_counter = last_frame - 5
        section = 3
        print(f'Ready to start on frame {frame_counter} to render {last_frame} and beyond.')
    frame_counter += 1
    last_frame_time = time.time()