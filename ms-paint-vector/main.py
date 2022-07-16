import datetime
import math
import os
import sys
import time
from math import atan2, ceil, cos, sin

import cv2
import keyboard
import numpy
import pyautogui
import win32api
import win32con
from PIL import Image

from constants import constants


def move(x: int, y: int):
	win32api.SetCursorPos((x, y))
def unclick():
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def click():
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)


def save_frame(frame: int, log=True):
	screenshot = pyautogui.screenshot()
	location = f'render-frames/{frame:04}.png'
	screenshot.save(location)
	if log: print(f'Saved frame {frame} at {location}')

def orientation(p1: tuple, p2: tuple, p3: tuple):
	val = (float(-p2[1] + p1[1]) * (p3[0] - p2[0])) - (float(p2[0] - p1[0]) * (-p3[1] + p2[1]))
	if val > 0: return 1   # cw
	elif val < 0: return 2 # ccw
	else: return 0         # col

def on_segment(start: tuple, end: tuple, point: tuple):
	if point[0] <= max(start[0], end[0]) and point[0] >= min(start[0], end[0]) and point[1] <= max(start[1], end[1]) and point[1] >= min(start[1], end[1]): return True
	else: return False

def lines_intersect(s1: tuple, e1: tuple, s2: tuple, e2: tuple):
	o1 = orientation(s1, e1, s2)
	o2 = orientation(s1, e1, e2)
	o3 = orientation(s2, e2, s1)
	o4 = orientation(s2, e2, e1)
	if o1 != o2 and o3 != o4: return True
	elif o1 == 0 and on_segment(s1, e1, s2): return True
	elif o2 == 0 and on_segment(s1, e1, e2): return True
	elif o3 == 0 and on_segment(s2, e2, s1): return True
	elif o4 == 0 and on_segment(s2, e2, e1): return True
	else: return False

def point_in_contour(point: tuple, contour: list):
	end_point = (10000 + constants.video_resolution[0], point[1] + 1)
	intersect_counter = 0
	for i in range(len(contour)):
		start = tuple(contour[i][0])
		k = (i + 1) % len(contour)
		end = tuple(contour[k][0])
		if lines_intersect(point, end_point, start, end):
			if orientation(start, point, end) == 0:
				if on_segment(start, end, point): return True
			intersect_counter += 1
	return intersect_counter % 2 != 0

def find_fill_point(contour: list):
	if len(contour) < 3: return None
	perp_add = None
	wind = 0
	for i in range(len(contour)):
		pt1 = tuple(contour[i][0])
		pt2 = tuple(contour[(i + 1) % len(contour)][0])
		pt3 = tuple(contour[(i + 3) % len(contour)][0])
		delta1 = (pt2[0] - pt1[0], -pt2[1] + pt1[1])
		delta2 = (pt3[0] - pt2[0], -pt3[1] + pt2[1])
		ang1 = atan2(delta1[1], delta1[0])
		ang2 = atan2(delta2[1], delta2[0])
		delta_ang = (ang2 - ang1) % (2 * math.pi)
		wind += delta_ang
	if wind > 0:
		perp_add = math.pi / 2  # CCW
	else:
		perp_add = -math.pi / 2 # CW

	for i in range(len(contour)):
		# Do meth
		pt1 = contour[i][0]
		pt2 = contour[(i + 1) % len(contour)][0]
		ang = atan2(-(pt2[1] - pt1[1]), pt2[0] - pt1[0])
		perp_ang = ang + perp_add
		x_off = ceil(constants.brush_size_offset) * cos(perp_ang)
		y_off = -ceil(constants.brush_size_offset) * sin(perp_ang)
		midpoint = ((pt1[0] + pt2[0]) / 2, (pt1[1] + pt2[1]) / 2)
		check_point = (round(midpoint[0] + x_off), round(midpoint[1] + y_off))
		point_in_outline = point_in_contour(check_point, contour)
		if point_in_outline: return check_point
	return None

def nested_contour(contour: list, contours: list):
	point = tuple(contour[0][0])
	count = 0
	for cont in contours:
		if cont.tolist() != contour and point_in_contour(point, cont.tolist()): count += 1
	return count

def draw_frame(frame: int):
	global frame_folder_path
	start_time = time.time()
	print(f'Proccessing frame {frame}')
	mat = cv2.imread(f'{frame_folder_path}{frame}.png', 0)
	ret, mat = cv2.threshold(mat, 100, 255, 0)
	mat = cv2.bitwise_not(mat)
	if not ret:
		print('Error: Threshold failed')
		return
	contours, hierarchy = cv2.findContours(mat, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# Debug here

	print(f'Drawing frame {frame}')
	
	# Change to pencil tool
	move(constants.pencil_position[0], constants.pencil_position[1])
	click()
	time.sleep(constants.sleep_time)
	unclick()
	for contour in contours:
		# break # To skip drawing
		as_list = None
		if type(contour) == list:
			as_list = contour
		else:
			as_list = contour.tolist()
		# Move to the first position and click
		move(as_list[0][0][0] + constants.canvas_position[0], as_list[0][0][1] + constants.canvas_position[1])
		time.sleep(constants.sleep_time)
		click()
		# Go through each point and move the cursor
		for i in range(len(as_list)):
			if keyboard.is_pressed('q'):
				unclick()
				sys.exit()
			if i + 1 >= len(as_list):
				i -= len(as_list)
			move(as_list[i + 1][0][0] + constants.canvas_position[0], as_list[i + 1][0][1] + constants.canvas_position[1])
			time.sleep(0.01)
		unclick()
	# return # To skip filling
	# Change to fill
	move(constants.fill_position[0], constants.fill_position[1])
	click()
	time.sleep(constants.sleep_time)
	unclick()
	for contour in contours:
		if keyboard.is_pressed('q'):
			unclick()
			sys.exit()
		as_list = None
		if type(contour) == list:
			as_list = contour
		else:
			as_list = contour.tolist()
		fill_point = find_fill_point(as_list)
		
		if fill_point == None: continue

		# Fill
		count = nested_contour(as_list, contours)
		if count % 2 == 0:
			time.sleep(constants.sleep_time)
			move(round(fill_point[0] + constants.canvas_position[0]), round(fill_point[1] + constants.canvas_position[1]))
			click()
			time.sleep(constants.sleep_time)
			unclick()
	move(constants.canvas_position[0] + constants.video_resolution[0] + 20, constants.canvas_position[1] + constants.video_resolution[1] + 20)
	save_frame(frame, log=False)
	print(f'Finished frame {frame} in {round(time.time() - start_time, 2)} seconds at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.')

frame_folder_path = os.getcwd()[:os.getcwd().rfind('\\')] + '\\frame-sequence\\'

print('Ready to go!')
while not keyboard.is_pressed('p'):
	if keyboard.is_pressed('q'): sys.exit()
while keyboard.is_pressed('p'):
	if keyboard.is_pressed('q'): sys.exit()

frame = 0
while not keyboard.is_pressed('q'):
	draw_frame(frame)