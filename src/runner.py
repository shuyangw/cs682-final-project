from gameread import GameReader
from actions import GameActions

import time 

class Runner(object):
    """
    This is the class that performs every action that we need depending on the
    result of the game reader.
    """
    def __init__(self, fps=15):
        print("Starting runner")
        self.fps = fps

    """
    The run method. This is the main loop that will perform every function that
    we may need.

    Input:
     - duration: An integer representing how long we would like our agent to
       run in seconds.
    """
    def run(self, duration=60):
        print("Runner running") 
        timer = time.time()
        GR = GameReader(self.fps, 15)
        GA = GameActions()
        iteration = 0
        while time.time() - timer < duration:
            #CRUCIAL
            iteration += 1
            GR.update_frames()

            