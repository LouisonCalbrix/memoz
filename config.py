'''
Global variables to be used by the memoz game.
date : April 2020
'''

import os

STAGE_SIZE = (700, 700)

# position
COORD_UP_LEFT = (0, 0)

# colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_ORANGE = (250, 147, 0)

# paths
RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
PATH_TILE_HIDDEN = os.path.join(RESOURCES, 'hidden-tile.png')
PATH_TILE_TARGET = os.path.join(RESOURCES, 'right-tile.png')
PATH_TILE_WRONG = os.path.join(RESOURCES, 'wrong-tile.png')
