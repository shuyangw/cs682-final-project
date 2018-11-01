from screen import grab_frame, get_window_pixels_mss

if __name__ == "__main__":
    for i in range(25):
        p = grab_frame(debug = False, wetime=True)