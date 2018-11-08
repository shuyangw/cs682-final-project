from gameread import GameReader

import time 

class Runner(object):
    """
    This is the class that performs every action that we need depending on the
    result of the hgame reader.
    """
    def __init__(self, fps=15):
        print("Starting runner")
        self.fps = fps

    """
    The run method. 
    """
    def run(self, duration=60):
        print("Runner running")
        timer = time.time()
        GR = GameReader(self.fps, 15)

        iteration = 0
        while time.time() - timer < duration:
            #CRUCIAL
            iteration += 1
            GR.update_frames()


            if iteration % 15 == 0:
                print(GR.isdead())