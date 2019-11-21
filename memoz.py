#! /usr/bin/env python3

# memoz
# A game where you need to use your short-term memory.
# The player is shown a grid made of tiles, most of them are blue and some
# of them are red. The player must remember where the red tiles are because,
# after a while, all the tiles are flipped and it is not possible to see which
# ones are red and which ones are blue. At that point, the player's goal is to
# click on the tiles that are red to get points, and since he doesn't have  
# unlimited tries he must choose wisely!
# date: November 2019

import pygame

class Tile:
    '''
    A Tile is a square that is either a target or not. The player must memorise
    the location of Tiles that are targets. When a Tile's _revealed attribute
    is True it is displayed so that we can differentiate between a target Tile
    and a non target one, when _revealed is False all the Tiles look the same.
    '''
    IMAGES = [
        pygame.image.load('resources/hidden-tile.png'),
        pygame.image.load('resources/right-tile.png'),
        pygame.image.load('resources/wrong-tile.png')
    ]


    def __init__(self, target, revealed):
        self._target = target
        self._revealed = revealed

    def draw_at(self, display_surface, window_coordinates):
        '''
        Choose the right picture to display and draw it on the display_surface
        at specified window_coordinates.
        '''
        if self._revealed:
            if self._target:
                display_img = Tile.IMAGES[1]
            else:
                display_img = Tile.IMAGES[2]
        else:
            display_img = Tile.IMAGES[0]
        display_surface.blit(display_img, window_coordinates)

    def reveal(self):
        '''
        Reveal the tile so when it is displayed on screen the player can see
        whether or not this is a target tile.
        '''
        pass

    def hide(self):
        '''
        Hide the tile so when it is displayed on screen the player is unable to
        see what kind of tile this is.
        '''
        pass
    
