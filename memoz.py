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

#constants
SIDE_TILE = 40
#WIDTH_TILE = 40
#HEIGHT_TILE = 40
MARGIN_TILE = 10

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
    '''
    A Grid is a set of tiles, that has both target tiles and other tiles. At
    the beginning of the game all tiles are revealed so the player can see
    and memorize them. Then, every tile of the Grid is hidden and at this 
    point the player needs to find back where the target tiles are.
    '''

    def __init__(self, height, width, nb_target, window_size):
        self._height = height
        self._width = width

        # geometry
        # calculate the margin between the window's edges and the grid's
        width_window, height_window = window_size
        width_grid = self._width * SIDE_TILE + (self._width - 1) * MARGIN_TILE
        height_grid = self._height * SIDE_TILE + (self._height - 1) * MARGIN_TILE
        self._margin = ((width_window - width_grid) // 2,
                        (height_window - height_grid) // 2)

        # randomly pick targets
        targets = sample([(i, j) for i in range(width) for j in range(height)],
                         nb_target)
        # create tiles
        self._tiles = []
        for j in range(height):
            a_row = []
            for i in range(width):
                if (i, j) in targets:
                    a_row.append(Tile(target=True, revealed=True))
                else:
                    a_row.append(Tile(target=False, revealed=True))
            self._tiles.append(a_row)

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

    def reveal_tile(self, row, column):
        '''
        Reveal tile sitting at (row, column).
        '''
        self[row, column].reveal()

    def tile_at(self, coords):
        '''
        Return the tile sitting at coords. coords are window coordinates.
        If there is no tile at this location, None is returned.
        '''
        # grid-wise coords 
        x_grid, y_grid = (coord-margin for coord, margin in zip(coords, self._margin))

        width_grid = self._width * SIDE_TILE + (self._width - 1) * MARGIN_TILE
        height_grid = self._height * SIDE_TILE + (self._height - 1) * MARGIN_TILE
        # check whether the cursor is in the grid area or not
        if 0 <= x_grid <= width_grid and 0 <= y_grid <= height_grid:
            # check whether the cursor is over a tile or the space between tiles
            if (x_grid % (SIDE_TILE+MARGIN_TILE) <= SIDE_TILE and
                y_grid % (SIDE_TILE+MARGIN_TILE) <= SIDE_TILE):
                column = x_grid // (SIDE_TILE+MARGIN_TILE)
                row = y_grid // (SIDE_TILE+MARGIN_TILE)
                # temporary return value for testing purpose
                return row, column
#                return self[row, column]
#        else:
#            return None

    def draw(self, surface):
        '''
        Draw the whole grid on the given surface.
        '''
        for i, row in enumerate(self._tiles):
            for j, tile in enumerate(row):
                x_window = self._margin[0] + j * (SIDE_TILE + MARGIN_TILE)
                y_window = self._margin[1] + i * (SIDE_TILE + MARGIN_TILE)
                tile.draw_at(surface, (x_window, y_window))

    def __getitem__(self, coords):
        return self.tiles[coords[0]][coords[1]]

    def __str__(self):
        res = ''
        for i in range(self.height):
            for j in range(self.width):
                res += '|{}'.format(self[i, j])

            res += '|\n'

        return res

class GameState:
    '''
    GameState is the class that encapsulate the game logic. It allows the player
    to interact with a game's grid and display that grid onscreen.
    '''

    def __init__(self, grid_dim, time, total_tries, screen):
        self._time = time           # time tiles will be revealed at the beginning
        self._grid_dim = grid_dim   # size of Grid instances 
        self._tries = total_tries   # number of tries before game over
        self._screen = screen
        pass

    def update(self):
        '''
        Method called once per frame, update every game component according to
        the user's input and time.
        '''
        # phase 1: reveal tiles until timer is 0
        if self._timer:
            self._timer -= 1
            # time's up hide all the tiles
            if self._timer == 0:
                self._grid.hide_all()

        # phase 2: player needs to find the good tiles
        else:
            # as long as there are remaining tries
            # capture mouse events?
            # if click: reveal tile at position?
            # if revealed tile is not target decrease remaining tries

        self.draw_game()     # draw game and relevent informations at every frame
        pass

    def start_game(self):
        '''
        Instanciate Grid, initialize _remaining_tries and timer.
        '''
        self._remaining_tries = self._tries   # current number of tries (to be decreased)
        self._timer = self._time              # timer (to be decreased) 
        window_size = self._screen.get_size()
        self._grid = Grid(*self._grid_gim, self._nb_target, window_size)
        pass

    def draw_timer(self):
        '''
        Draw onscreen a representation of the time remaining during which
        tiles are all revealed.
        '''
        pass
    
    def draw_game(self):
        '''
        Draw grid, remaining tries, timer(, points?)
        '''
        pass

    # factories
    @classmethod
    def EasyGame(cls):
        pass

    @classmethod
    def NormalGame(cls):
        pass

    @classmethod
    def HardGame(cls):
        pass
