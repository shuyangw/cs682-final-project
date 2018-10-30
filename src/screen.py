import win32gui
import sys
import time
import numpy as np

from PIL import ImageGrab
"""
Converts a given pixel in the form (R, G, B) to a single pixel representing
its value in grayscale from 0-255 following the equation:
	grayscale_pixel = R*0.21 + G*0.572 + B*0.07
from the article:
https://www.johndcook.com/blog/2009/08/24/algorithms-convert-color-grayscale/

Inputs:
 - pixel: A 3-tuple representing a pixel in (R, G, B)

Returns an integer from 0-255 representing a grayscale version of the pixel

"""
def rgb_to_grayscale(pixel):
	return pixel[0] * 0.21 + pixel[1] * 0.572 + pixel[2] * 0.07

"""
Performs a O(lw) scan over the given input rectangle to grab the pixels in
grayscale of the screen.

Inputs:
 - rect: A 4-tuple representing the coordinates that define the rectangle on the
   screen.

Returns an array representing the grayscale pixels of the screen given the
rectangle of shape (l, w).
"""
def get_window_pixels(rect):
	count = 0
	pixels = ImageGrab.grab().load()
	x_range, y_range = rect[2] - rect[0], rect[3] - rect[1]
	start_x, start_y = rect[0], rect[1]
	export_pixels = [[0 for y in range(y_range)] for x in range(x_range)]
	for y in range(rect[1], rect[3]):
		for x in range(rect[0], rect[2]):
			export_pixels[x-start_x][y-start_y] = rgb_to_grayscale(pixels[x,y])
	return np.array(export_pixels)

"""
Obtains the list of Windows hwnds given a string representing the title of the
desired process. We will return every process with the exact string if the 
"exact" parameter is True. If not, we return every process with that string in
the name.

Inputs:
 - title_text: A string representing a desired string.
 - exact: A boolean representing whether or not we want to find the exact
   string within the process name.

Returns a list of process names that we could possible want.
"""
def _get_windows_by_title(title_text, exact = False):
	def _window_callback(hwnd, all_windows):
		all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
	windows = []
	win32gui.EnumWindows(_window_callback, windows)
	if exact:
		return [hwnd for hwnd, title in windows if title_text == title]
	else:
		return [hwnd for hwnd, title in windows if title_text in title]

"""
Returns the rectangle that defines the process we want. For the purpose of this
project, we simply grab the game window.
"""
def get_window_rect():
	hwndList = _get_windows_by_title("THUMPER")
	try:
		hwnd = hwndList[0]
	except(IndexError):
		print("Error: Window not found. Please make sure game is launched.")
		sys.exit()

	#Sets window to be in front
	try:
		win32gui.SetForegroundWindow(hwnd)
	except:
		print("Unexpected error, please restart Minesweeper and retry")
		sys.exit()

	rect = win32gui.GetWindowRect(hwnd)

	negatives = 0
	for element in rect:
		if element < 0:
			negatives += 1 	
	if negatives == 4:
		print("Unexpected error, please restart game retry")
		sys.exit()
	return rect