import numpy as np
import queue

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
     - max_frame_storage: An integer represeting how many frames we will be
       holding in memory.
    """
    def __init__(self, fps, max_frame_storage):
        self.fps = fps
        self.frame_queue = queue.Queue(maxsize=max_frame_storage)

    """
    Grabs the next frame in the game and updates the frame queue. The frame
    queue must not have more than 20 frames. If it is full, we discard the 
    oldest frame and insert the newest one.

    Returns the oldest frame in the queue.
    """
    def update_frame_queue(self):
        popped_frame = None
        if not self.frame_queue.empty():
            frame = grab_frame()
            if self.frame_queue.full():
                popped_frame = self.frame_queue.get()
                self.frame_queue.put(frame)
            else:
                self.frame_queue.put(frame)
        return return_item

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
    """
    def parse_frame(self):
        pass