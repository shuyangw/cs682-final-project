import numpy as np
import queue

from scipy.misc import imsave

from screen import grab_frame

class GameReader(object):
    """
    The GameReader object parses 15 frames at a time and returns the game state
    that shall be interpreted by the game loop.

    Constructor initializes the object, frame rate and the queue that stores 
    our frames.

    Inputs:
     - fps: An integer represeting how many frames we would like to read per 
       second.
     - max_queue_size: An integer represeting how many frames we will be
       holding in memory.
    """
    def __init__(self, fps, max_queue_size):
        self.fps = fps
        self.max_queue_size = max_queue_size
        self.frame_queue = queue.Queue(maxsize=max_queue_size)
        self.frame_shape = None
        self.is_dead = False

        #To debug frames
        self.imsave_img_count = 0
        self.imsave_queue_count = 0
        self.save_dir = "../debug_frames/"

    """
    Grabs the next frame in the game and updates the frame queue. The frame
    queue must not have more than 20 frames. If it is full, we discard the 
    oldest frame and insert the newest one.

    Returns the oldest frame in the queue.
    """
    def update_frames(self):
        popped_frame = None
        frame = grab_frame()
        if self.frame_shape == None:
            self.frame_shape = frame.shape
        if self.frame_queue.full():
            popped_frame = self.frame_queue.get()
            self.frame_queue.put(frame)
        else:
            self.frame_queue.put(frame)
        return popped_frame

    """
    Returns the average grayscale value from every pixel curerntly stored in the
    frame queue.
    """
    def avg_luminosity(self):
        frame_length = float(len(self.frame_queue))
        return np.sum(np.array(list(self.frame_queue.queue))) / frame_length

    """
    Returns whether or not the player is dead, indicating the restarting of a
    new trial.
    """
    def isdead(self):
        if self.frame_shape == None:
            return True
        prev_frame_val = np.inf
        flag_count = 0
        for img in list(self.frame_queue.queue):
            #Sum up every pixel value
            W, H = self.frame_shape
            frame_val = float(np.sum(img)) / (W * H)
            print(frame_val)

            """
            For some reason, the screen that appears when the player loses, 
            appears to be perfect black to the naked eye, but is in actuality,
            no where near. The screen has a grayscale value of about 13 out of
            a maximum 255.
            """
            if frame_val < 0.06:
                return True
        return False
    """
    Analyzes the queue of frames and returns the state of the game.
    
    TODO: Need to possibly update
    Here are the prospective states 
     - playing: The agent is current in play and is running normally. In other
       words, the player is currently acting normally and is neither dead,
       recovering dead nor transitioning from level to level.
     - dead: The agent has made a mistake and is now resetting itself to be
       playing again. 
     - transition: The game is now in a transitional phase and we must wait 
       until it is not to begin acting again.
       # NOTE: Might not need this
    """
    def parse(self):
        pass

    def save_queue(self):
        for img in list(self.frame_queue.queue):
            img_name = ("queue" + str(self.imsave_queue_count) + "img" +
                str(self.imsave_img_count) + ".png")
            
            mod_dir = self.save_dir + img_name
            print("Saving" + img_name)
            imsave(mod_dir, img)

            self.imsave_img_count += 1
        self.imsave_queue_count += 1
