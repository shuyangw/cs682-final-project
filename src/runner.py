from gameread import GameReader

class Runner(object):
    """
    This is the class that performs every action that we need depending on the
    result of the hgame reader.
    """
    def __init__(self, fps=15):
        self.fps = fps

    """
    The run method. 
    """
    def run(self, duration=60):
        pass