import time
import keyboard
import win32api, win32con
import sys
from PIL import Image
import numpy
import pyautogui
from math import floor

def click_board(x: int, y: int, left: bool):
	global region, tile_size
	win32api.SetCursorPos((x * tile_size + region[0], y * tile_size + region[1]))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN if left else win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
	time.sleep(0.01) # Seconds
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP if left else win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

def quit():
	print(f'Exiting on frame {frame_counter}')
	sys.exit()

def pause():
	while keyboard.is_pressed('p'):
		if keyboard.is_pressed('q'): quit()
	while not keyboard.is_pressed('p'):
		if keyboard.is_pressed('q'): quit()
	while keyboard.is_pressed('p'):
		if keyboard.is_pressed('q'): quit()

def render_frame(frame: list):
	global video_resolution
	freq = video_resolution[0] / render_resolution[0]
	to_print = ''
	sub_x = 0
	sub_y = 0
	click_count = 0
	for y in range(len(frame)):
		if y % freq != 0:
			continue
		for x in range(len(frame[y])):
			if keyboard.is_pressed('p'): pause()
			elif keyboard.is_pressed('q'): quit()
			if x % freq != 0:
				continue
			if (frame[y][x][0] >= 128) != board[sub_y + top_margin][sub_x]:
				board[(sub_y + top_margin)][sub_x] = not board[sub_y + top_margin][sub_x]
				click_board(sub_x, sub_y + top_margin, False)
				click_count += 1
			sub_x += 1
		sub_y += 1
		sub_x = 0

def read_board():
	global board, region, tile_size
	# Get a screenshot of the board area and create the board variable
	img = pyautogui.screenshot(region=region)
	board = [[True] * 24 for _ in range(20)]
	for y in range(len(board)):
		search_y = y * tile_size + (0.41 * tile_size)
		for x in range(len(board[y])):
			search_x = x * tile_size + (0.44 * tile_size)
			board[y][x] = False if img.getpixel((search_x, search_y))[0] - 242 <= 3 else True

# Easy (210%)
# region = (486, 269, (1416 - 486), (1013 - 269))p
# dimens = (10, 8)
# render_res = (10, 8)

# Medium (170%)
# region = (489, 271, (1413 - 489), (990 - 271))
# dimens = (18, 14)
# render_res = (18, 14)

# Hard (160%)
region = (478, 239, 946, 790)
dimens = (24, 20)
render_resolution = (24, 18)

top_margin = round((dimens[1] - render_resolution[1]) / 2)
video_resolution = (960, 720)
board = [[True] * 24 for _ in range(20)]
tile_size = round(region[3] / dimens[1])


# Wait until P is pressed and un-pressed for the user to switch to Paint before starting.
while not keyboard.is_pressed('p'):
	if keyboard.is_pressed('q'): quit()
while keyboard.is_pressed('p'):
	if keyboard.is_pressed('q'): quit()

read_board()
# frame_counter = 243
frame_counter = 150
running = True # Loop variable
last_frame_time = time.time() # To get frame time (generally around a minute)
while running:
	img = Image.open(f'./frame-sequence/{frame_counter:04}.png')
	frame = numpy.asarray(img)

	prev_board = board
	render_frame(frame)
	if board != prev_board:
		win32api.SetCursorPos((130, 85))
		time.sleep(1.2)

	screenshot = pyautogui.screenshot()
	screenshot.save(f'render-frames/{frame_counter:04}.png')
	print(f'Finished frame {frame_counter:04} in {time.time() - last_frame_time} seconds.')
	frame_counter += 1
	last_frame_time = time.time()