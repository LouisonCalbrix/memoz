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
from random import sample

class Tile:
    '''
    A Tile is a square that is either a target or not. The player must memorise
    the location of Tiles that are targets. When a Tile's _revealed attribute
    is True it is displayed so that we can differentiate between a target Tile
    and a non target one, when _revealed is False all the Tiles look the same.
    '''

    IMG_HIDDEN = pygame.image.load('resources/hidden-tile.png')
    IMG_TARGET = pygame.image.load('resources/right-tile.png')
    IMG_WRONG = pygame.image.load('resources/wrong-tile.png')


    def __init__(self, target, revealed):
        '''
        Initialisation of a tile, target and revealed are both expected to be
        booleans.
        '''
        self._target = target
        self._revealed = revealed

    def draw_at(self, display_surface, window_coordinates):
        '''
        Choose the right picture to display and draw it on the display_surface
        at specified window_coordinates.
        '''
        if self._revealed:
            if self._target:
                display_img = Tile.IMG_TARGET
            else:
                display_img = Tile.IMG_WRONG
        else:
            display_img = Tile.IMG_HIDDEN
        display_surface.blit(display_img, window_coordinates)


    @property
    def target(self):
        return self._target
    
    @property
    def revealed(self):
        return self._revealed
    
    @revealed.setter
    def revealed(self, value):
        self._revealed = value


    def reveal(self):
        '''
        Reveal the tile so when it is displayed on screen the player can see
        whether or not this is a target tile.
        '''
        self.revealed = True

    def hide(self):
        '''
        Hide the tile so when it is displayed on screen the player is unable to
        see what kind of tile this is.
        '''
        self.revealed = False
    
    def flip(self):
        '''
        Flip the tile so, if it's hidden, it gets revealed and the other way 
        around.
        '''
        self.revealed = not self.revealed

    def __str__(self):
        if (self.revealed):
            if (self.target):
                return 'O'
            else:
                return 'X'
        else:
            return ' '


class Grid(object):
    """docstring for Grid"""
    def __init__(self, height, width, nb_target):
        self._height = height
        self._width = width

        # randomly picks targets
        targets = sample([(i, j) for i in range(width) for j in range(height)],
                         nb_target)

        self._tiles = []
        for j in range(height):
            a_row = []
            for i in range(width):
                if (i, j) in targets:
                    a_row.append(Tile(target=True, revealed=False))
                else:
                    a_row.append(Tile(target=False, revealed=False))
            self._tiles.append(a_row)
#        self._tiles = ([
#            [Tile(target=False, revealed=False) for _ in range(width)]
#            for _ in range(height)
#        ])


    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def tiles(self):
        return self._tiles

    def reveal_all(self):
        '''
        Reveal every tile of the grid.
        '''
        for row in self._tiles:
            for tile in row:
                tile.reveal()

    def hide_all(self):
        '''
        Hide every tile of the grid.
        '''
        for row in self._tiles:
            for tile in row:
                tile.hide()

    def __getitem__(self, coords):
        return self.tiles[coords[0]][coords[1]]

    def __str__(self):
        res = ''
        for i in range(self.height):
            for j in range(self.width):
                res += '|{}'.format(self[i, j])

            res += '|\n'

        return res
