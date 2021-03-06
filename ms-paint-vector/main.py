import datetime
import math
import os
import sys
import time
from math import atan2, ceil, cos, sin, sqrt

import cv2
import keyboard
import pyautogui
import win32api
import win32con

from constants import constants


def move(x: int, y: int):
	win32api.SetCursorPos((x, y))
def unclick():
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def click():
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

def resize_bigger():
	time.sleep(0.2)
	move(constants.canvas_position[0] + constants.video_resolution[0], constants.canvas_position[1] + constants.video_resolution[1])
	click()
	time.sleep(0.2)
	move(constants.canvas_position[0] + constants.video_resolution[0] + 30, constants.canvas_position[1] + constants.video_resolution[1] + 30)
	time.sleep(0.2)
	unclick()
	time.sleep(0.2)

def resize_smaller():
	time.sleep(0.2)
	move(constants.canvas_position[0] + constants.video_resolution[0] + 30, constants.canvas_position[1] + constants.video_resolution[1] + 30)
	click()
	time.sleep(0.2)
	move(constants.canvas_position[0] + constants.video_resolution[0], constants.canvas_position[1] + constants.video_resolution[1])
	time.sleep(0.2)
	unclick()
	time.sleep(0.2)

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

def point_seg_dist(point: tuple, p1: tuple, p2: tuple):
	if p1[0] == p2[0]: # Vertical line, infinite slope
		hoz_dist = abs(point[0] - p2[0])
		vert_dist = min(abs(p1[1] - point[1]), abs(p2[1] - point[1]))
		return sqrt(hoz_dist**2 + vert_dist**2)
	elif p1[1] == p2[1]: # Horizontal line, zero slope
		vert_dist = abs(point[1] - p2[1])
		hoz_dist = min(abs(p1[0] - point[0]), abs(p2[0] - point[0]))
		return sqrt(hoz_dist**2 + vert_dist**2)
	else:
		m_0 = (p2[1] - p1[1]) / (p2[0] - p1[0])
		b_0 = p1[1] - m_0 * p1[0]
		m_1 = -1 / m_0
		b_1 = point[1] - m_1 * point[0]
		intersect_x = (b_1 - b_0) / (m_0 - m_1)
		intersect_y = m_0 * intersect_x + b_0
		perp_dist = sqrt((point[0] - intersect_x)**2 + (point[1] - intersect_y)**2)
		check_1 = (p1[0] + 1, p1[1] + m_1)
		check_2 = (p2[0] + 1, p2[1] + m_1)
		o_1 = orientation(p1, check_1, point)
		o_2 = orientation(p2, check_2, point)
		if o_1 != o_2 or o_1 == 0 or o_2 == 0:
			# print(f'returning perp dist')
			return perp_dist
		par_dist = min(sqrt((intersect_x - p1[0])**2 + (intersect_y - p1[1])**2), sqrt((intersect_x - p2[0])**2 + (intersect_y - p2[1])**2))
		# par_dist = 0
		return sqrt(par_dist**2 + perp_dist**2)

def point_poly_dist(point: tuple, contour: list):
	min_dist = 100000
	smallest_index = 0
	for i in range(len(contour)):
		pt1 = contour[i][0]
		pt2 = contour[(i + 1) % len(contour)][0]
		dist = point_seg_dist(point, pt1, pt2)
		min_dist = min(min_dist, dist)
		if min_dist == dist: smallest_index = i
		# print(f'dist {dist}, min {min_dist}')
	# print(smallest_index)
	return min_dist

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

	final_point = None
	for i in range(len(contour)):
		# Do meth
		pt1 = contour[i][0]
		pt2 = contour[(i + 1) % len(contour)][0]
		ang = atan2(-(pt2[1] - pt1[1]), pt2[0] - pt1[0])
		perp_ang = ang + perp_add
		x_off = constants.brush_size_offset * cos(perp_ang)
		y_off = -constants.brush_size_offset * sin(perp_ang)
		midpoint = ((pt1[0] + pt2[0]) / 2, (pt1[1] + pt2[1]) / 2)
		check_point = (round(midpoint[0] + x_off), round(midpoint[1] + y_off))
		# if i == 3:
		# 	return check_point
		point_in_outline = point_in_contour(check_point, contour)
		if point_in_outline:
			dist = point_poly_dist(check_point, contour)
			# print(f'dist {i} {len(contour)}: {dist}')
			if dist >= sqrt(2): final_point = check_point; break
	# if final_point != None:
		# print(f'dist {len(contour)}: {point_poly_dist(final_point, contour)} pixels')
	return final_point

def nested_contour(contour: list, contours: list):
	point = tuple(contour[0][0])
	count = 0
	for cont in contours:
		if cont.tolist() != contour and point_in_contour(point, cont.tolist()): count += 1
	return count

def new_file():
	time.sleep(0.2)
	move(constants.file_position[0], constants.file_position[1])
	click()
	time.sleep(0.2)
	unclick()
	time.sleep(0.2)
	move(constants.new_position[0], constants.new_position[1])
	click()
	time.sleep(0.2)
	unclick()
	time.sleep(0.2)
	move(constants.no_save_position[0], constants.no_save_position[1])
	click()
	time.sleep(0.2)
	unclick()
	time.sleep(0.2)

def draw_frame(frame: int):
	global frame_folder_path
	start_time = time.time()

	print(f'Proccessing frame {frame}')
	mat = cv2.imread(f'{frame_folder_path}{frame:04}.png', 0)
	ret, mat = cv2.threshold(mat, 100, 255, 0)
	mat = cv2.bitwise_not(mat)
	if not ret:
		print('Error: Threshold failed')
		return
	contours, hierarchy = cv2.findContours(mat, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# Debug here
	# print(len(contours))
	# print(f'two = {contours[2].tolist()}')
	# print(f'one = {contours[1].tolist()}')
	# return

	print(f'Drawing frame {frame}')
	
	new_file()
	resize_bigger()
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
		fill_x, fill_y = fill_point[0], fill_point[1]
		fill_x = min(max(fill_x, 1), constants.video_resolution[0] - 1)
		fill_y = min(max(fill_y, 1), constants.video_resolution[1] - 1)
		fill_point = (fill_x, fill_y)

		print(f'fill point for len {len(contour.tolist())}: {fill_point}')

		# Fill
		count = nested_contour(as_list, contours)
		if count % 2 == 0:
			time.sleep(constants.sleep_time)
			move(round(fill_point[0] + constants.canvas_position[0]), round(fill_point[1] + constants.canvas_position[1]))
			click()
			time.sleep(constants.sleep_time)
			unclick()
	resize_smaller()
	move(constants.canvas_position[0] + constants.video_resolution[0] + 30, constants.canvas_position[1] + constants.video_resolution[1] + 30)
	# save_frame(frame, log=False)
	print(f'Finished frame {frame} in {round(time.time() - start_time, 2)} seconds at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.')

frame_folder_path = os.getcwd()[:os.getcwd().rfind('\\')] + '\\frame-sequence\\'

print('Ready to go!')
while not keyboard.is_pressed('p'):
	if keyboard.is_pressed('q'): sys.exit()
while keyboard.is_pressed('p'):
	if keyboard.is_pressed('q'): sys.exit()

# frame = 1387
# while not keyboard.is_pressed('q'):
# 	draw_frame(frame)
	# frame += 1
draw_frame(1388)
