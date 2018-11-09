import pyautogui
import numpy as np

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
            "air": self.air,
            "sleft": self.slide_left,
            "sright": self.slide_right,
            "stomp": self.stomp,
            "stompa": self.stomp_air,
            "pass": self.nothing
        }
        self.arrow_key_down = False
        self.which_key_down = None
        self.space_down = False

    """
    Performs an action at random.
    """
    def random_action(self, verbose=False):
        action_index = np.random.randint(0, len(self.actions))
        action_name = list(self.actions)[action_index]
        if verbose:
            print("Performing action:", action_name)
        action = self.actions[action_name]
        action()

    """
    Corresponds to the action that shifts the player left.
    Conforms to the right arrowkey.
    """
    def move_right(self):
        if not self.arrow_key_down:
            pyautogui.keyDown('right')
            self.arrow_key_down = True
            self.which_key_down = 'right'
        else:
            if self.which_key_down == 'right':
                pyautogui.keyUp('right')
                self.which_key_down = None
                self.arrow_key_down = False
            else:
                pyautogui.keyUp(self.which_key_down)
                pyautogui.keyDown('right')
                self.which_key_down = 'right'

    """
    Corresponds to the action that shifts the player left.
    Conforms to the left arrowkey.
    """
    def move_left(self):
        if not self.arrow_key_down:
            pyautogui.keyDown('left')
            self.arrow_key_down = True
            self.which_key_down = 'left'
        else:
            if self.which_key_down == 'left':
                pyautogui.keyUp('left')
                self.which_key_down = None
                self.arrow_key_down = False
            else:
                pyautogui.keyUp(self.which_key_down)
                pyautogui.keyDown('left')
                self.which_key_down = 'left'
    
    def air(self):
        if not self.arrow_key_down:
            pyautogui.keyDown('up')
            self.arrow_key_down = True
            self.which_key_down = 'up'
        else:
            if self.which_key_down == 'up':
                pyautogui.keyUp('up')
                self.which_key_down = None
                self.arrow_key_down = False
            else:
                pyautogui.keyUp(self.which_key_down)
                pyautogui.keyDown('up')
                self.which_key_down = 'up'

    """
    Corresponds to the action that slides the player left.
    Conforms to combination: left + spacebar
    """
    def slide_left(self):
        self.move_left()
        self.stomp()
    """
    Corresponds to the action that slides the player left.
    Conforms to combination: right + spacebar
    """
    def slide_right(self):
        self.move_right()
        self.stomp()

    """
    Corresponds to the action that performs the stomp action.
    Conforms to the spacebar.
    """
    def stomp(self):
        if not self.space_down:
            pyautogui.keyDown('space')
            self.space_down = True
        else:
            pyautogui.keyDown('space')
            self.space_down = False

    """
    Corresponds to the action that performs the stomp when the player is
    initially in mid-air.
    Conforms to combination: down + spacebar
    """
    def stomp_air(self):
        self.stomp()
        self.air()

    """
    Clears every ongoing action.
    """
    def nothing(self):
        pyautogui.keyUp('space')
        if self.which_key_down != None:
            pyautogui.keyUp(self.which_key_down)