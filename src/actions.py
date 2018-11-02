import pyautogui

class GameActions(object):
    """
    Defines the actions that can be taken by the agent into the game. 
    Constructor initializes a dictionary that serves as a way to easily access
    the actions that can be taken.
    """
    def __init__(self):
        self.actions = {
            "left": self.move_left,
            "right": self.move_right,
            "sleft": self.slide_left,
            "sright": self.slide_right,
            "stomp": self.stomp,
            "stompa": self.stomp_air,
            "ground": self.ground,
            "pass": self.nothing
        }
        self.arrow_key_down = False
        self.space_down = False

    """
    Corresponds to the action that shifts the player left.
    Conforms to the right arrowkey.
    """
    def move_right(self):
        pass

    """
    Corresponds to the action that shifts the player left.
    Conforms to the left arrowkey.
    """
    def move_left(self):
        pass
    
    """
    Corresponds to the action that slides the player left.
    Conforms to combination: left + spacebar
    """
    def slide_left(self):
        pass

    """
    Corresponds to the action that slides the player left.
    Conforms to combination: right + spacebar
    """
    def slide_right(self):
        pass

    """
    Corresponds to the action that performs the stomp action.
    Conforms to the spacebar.
    """
    def stomp(self):
        pass

    """
    Corresponds to the action that performs the stomp when the player is
    initially in mid-air.
    Conforms to combination: down + spacebar
    """
    def stomp_air(self):
        pass

    """
    Does nothing to the game.
    """
    def nothing(self):
        pass