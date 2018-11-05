import win32gui
import sys
import time
import numpy as np

from PIL import ImageGrab, Image

first_time_running = True
window_rect = 0

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
Grabs the pixels in grayscale of the screen or in color if needed.

Inputs:
 - rect: A 4-tuple representing the coordinates that define the rectangle on the
   screen.

Returns an array representing the grayscale pixels of the screen given the
rectangle of shape (l, w).
"""
def get_window_pixels(rect, grayscale=True):
	if not grayscale:
		return ImageGrab.grab(bbox=tuple(rect))
	else:
		return ImageGrab.grab(bbox=tuple(rect)).convert("L")

"""
Does the same thing as get_window_pixels() but with a faster method. Extracts
a pixel in about 0.03 of a second.
"""
def get_window_pixels_mss(rect):
	from mss import mss
	with mss() as sct:
		bound = { 	"top": rect[1],
					"left": rect[0],
					"width": rect[2] - rect[0],
					"height": rect[3] - rect[1],
					"mon": len(sct.monitors) - 1
		}
		sct_img = sct.grab(bound)
		return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

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
def _get_windows_by_title(title_text, exact=False):
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
		print("Unexpected error, please restart game and retry")
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

"""
Returns the current game frame in the form of an array of grayscale pixels.

Inputs:
 - grayscale: A boolean representing whether or not we want our frame to be in
   grayscale. In our context, we would typically want this to be true unless
   we're debugging this method.
 - wetime: A boolean representing if we want to time the function of grabbing
   a frame. Typically only use this for debugging as well.
"""
def grab_frame(grayscale=True, wetime=False):
	global window_rect
	if window_rect == 0:
		window_rect = get_window_rect()
	now = 0
	if wetime:
		now = time.time()		
	pixels = None
	if grayscale:
		pixels = get_window_pixels_mss(window_rect, grayscale).convert("L")
	else:
		pixels = get_window_pixels_mss(window_rect, grayscale)
	if debug:
		if wetime:
			now = time.time()
		pixels.show()
		if wetime:
			print("Showing frame. Took time:", time.time()-now)
	if wetime:
		print("Grabbing frame. Took time:", time.time()-now)

	#Return normalized frame
	return np.array(pixels) / 255.
