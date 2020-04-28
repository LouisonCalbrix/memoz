'''
Global variables to be used by the memoz game.
date : April 2020
'''

import os

# size of the window
STAGE_SIZE = (700, 700)

# position
COORD_UP_LEFT = (0, 0)

# framerate
FPS = 40

# colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_ORANGE = (250, 147, 0)
COLOR_YELLOW = (255, 220, 58)
COLOR_BLUE_1 = (67, 137, 215)
COLOR_BLUE_2 = (56, 116, 181)

# paths
RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
PATH_TILE_HIDDEN = os.path.join(RESOURCES, 'hidden-tile.png')
PATH_TILE_TARGET = os.path.join(RESOURCES, 'right-tile.png')
PATH_TILE_WRONG = os.path.join(RESOURCES, 'wrong-tile.png')
FONT_TITLE = os.path.join(RESOURCES, 'LeagueSpartan-Bold.otf')
FONT_PRIM = os.path.join(RESOURCES, 'Comic_Sans_MS.ttf')
FONT_SIZE_1 = 72
FONT_SIZE_2 = 46
