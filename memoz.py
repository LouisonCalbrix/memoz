#! /usr/bin/env python3

# memoz
# A game where you need to use your short-term memory.
# The player is shown a grid made of tiles, most of them are blue and some
# of them are yellow. The player must remember where the yellow tiles are because,
# after a while, all the tiles are flipped and it is not possible to see which
# ones are yellow and which ones are blue. At that point, the player's goal is to
# click on the tiles that are yellow to get points, and since he doesn't have  
# unlimited tries he must choose wisely!
# date: November 2019

import pygame
import utils
from random import sample
from config import *

MARGIN_TILE = 10

class Tile:
    '''
    A Tile is a square that is either a target or not. The player must memorise
    the location of Tiles that are targets. When a Tile's _revealed attribute
    is True it is displayed so that we can differentiate between a target Tile
    and a non target one, when _revealed is False all the Tiles look the same.
    '''

    IMG_HIDDEN = pygame.image.load(PATH_TILE_HIDDEN)
    IMG_TARGET = pygame.image.load(PATH_TILE_TARGET)
    IMG_WRONG = pygame.image.load(PATH_TILE_WRONG)
    # raise error if all three images are not the same size
    if (IMG_HIDDEN.get_size() != IMG_TARGET.get_size() or
        IMG_TARGET.get_size() != IMG_WRONG.get_size()):
        raise ValueError('Images used should be the same size (pixel-wise)')
    # raise error if images are not square
    if IMG_HIDDEN.get_width() != IMG_HIDDEN.get_height():
        raise ValueError('Square images expected')
    SIDE_TILE = IMG_HIDDEN.get_width()


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
        if not self.revealed:
            self.revealed = True
            return self.target
        else:
            return True

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
        width_grid = self._width * Tile.SIDE_TILE + (self._width - 1) * MARGIN_TILE
        height_grid = self._height * Tile.SIDE_TILE + (self._height - 1) * MARGIN_TILE
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

    @property
    def points(self):
        '''
        Return number of revealed tiles that are targets.
        '''
        flatten = [tile for row in self.tiles for tile in row if tile.revealed and tile.target]
        return len(flatten)

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

    def reveal_tile(self, coords):
        '''
        Reveal tile sitting at (row, column).
        '''
        tile = self.tile_at(coords)
        return tile.reveal()

    def tile_at(self, coords):
        '''
        Return the tile sitting at coords. coords are window coordinates.
        If there is no tile at this location, None is returned.
        '''
        # grid-wise coords 
        x_grid, y_grid = (coord-margin for coord, margin in zip(coords, self._margin))

        width_grid = self._width * Tile.SIDE_TILE + (self._width - 1) * MARGIN_TILE
        height_grid = self._height * Tile.SIDE_TILE + (self._height - 1) * MARGIN_TILE
        # check whether the cursor is in the grid area or not
        if 0 <= x_grid <= width_grid and 0 <= y_grid <= height_grid:
            # check whether the cursor is over a tile or the space between tiles
            if (x_grid % (Tile.SIDE_TILE+MARGIN_TILE) <= Tile.SIDE_TILE and
                y_grid % (Tile.SIDE_TILE+MARGIN_TILE) <= Tile.SIDE_TILE):
                column = x_grid // (Tile.SIDE_TILE+MARGIN_TILE)
                row = y_grid // (Tile.SIDE_TILE+MARGIN_TILE)
                # temporary return value for testing purpose
#                return row, column
                return self[row, column]

    def draw(self, surface):
        '''
        Draw the whole grid on the given surface.
        '''
        for i, row in enumerate(self._tiles):
            for j, tile in enumerate(row):
                x_window = self._margin[0] + j * (Tile.SIDE_TILE + MARGIN_TILE)
                y_window = self._margin[1] + i * (Tile.SIDE_TILE + MARGIN_TILE)
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

class GameScene(utils.Scene):
    '''
    GameScene is the class that encapsulate the game logic. It allows the player
    to interact with a game's grid and display that grid onscreen.
    '''
    # height of the time relatively to the height of the whole screen (in %)
    TIMER_REL_HEIGHT = 2
    TIMER_ABS_HEIGHT = 0                  # to be initialized 

    def __init__(self, stage, grid_dim=(2, 2), nb_target=2, time=2,
                 total_tries=3, lives=3):
        super().__init__(stage)
        self._time = time           # time tiles will be revealed at the beginning
        self._difficulty = 0
        self._grid_dim = grid_dim   # size of Grid instances 
        self._nb_target = nb_target
        self._tries = total_tries   # number of tries before game over
        self._lives = lives         # number of game that can be lost before back to menu
        self._remaining_lives = lives
        self._game_over = True
        type(self).TIMER_ABS_HEIGHT = self.TIMER_REL_HEIGHT * self._stage.screen.get_height() // 100

    # Implementation of Scene abstract methods

    def handle_inputs(self, inputs):
        # start new game
        if self._game_over:
            self.start_game()
        # phase 1: reveal tiles until timer is 0
        if self._timer:
            self._timer -= 1
            # time's up hide all the tiles
            if self._timer == 0:
                self._grid.hide_all()

        # phase 2: player needs to find the good tiles
        else:
            for an_input in inputs:
                # as long as there are remaining tries
                # if click: reveal tile at this position
                # if revealed tile is not target decrease remaining tries
                # game over if no tries left or all target tiles have been found
                if an_input.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    try:
                        if not self._grid.reveal_tile(pos):        # wrong tile!
                            self._remaining_tries -= 1

                        if not self._remaining_tries:              # lost game
                            self.difficulty -= 1
                            self._game_over = True               
                            self.lives -= 1
                        elif self._grid.points == self.nb_target:  # won game
                            self.difficulty += 1
                            self._game_over = True
                    # mouse clicked while not over a tile
                    except AttributeError:
                        pass

    def draw(self):
        '''
        Draw grid, remaining tries, timer(, points?)
        '''
        self._stage.screen.fill(COLOR_BLACK)
        self.draw_timer()
        self.draw_tries()
        self._grid.draw(self._stage.screen)

    # Drawing sub-methods

    def draw_tries(self):
        '''
        Write onscreen how many tries does the player have left.
        '''
        font = pygame.font.Font(None, 55)
        txt_surf = font.render(str(self._remaining_tries), True, COLOR_ORANGE)
        self._stage.screen.blit(txt_surf, (0,0))

    def draw_timer(self):
        '''
        Draw onscreen a representation of the time remaining during which
        tiles are all revealed.
        '''
        if self._timer:
            width = int((self._timer / self._time) * self._stage.screen.get_width()) 
            rect = pygame.Rect(0, self._stage.screen.get_height()-self.TIMER_ABS_HEIGHT, 
                               width, self.TIMER_ABS_HEIGHT)
            pygame.draw.rect(self._stage.screen, COLOR_ORANGE, rect)
    
    # Own functionnalities

    def start_game(self):
        '''
        Instanciate Grid, initialize _remaining_tries and timer.
        '''
        self._game_over = False
        self._remaining_tries = self._tries   # current number of tries (to be decreased)
        self._timer = self._time              # timer (to be decreased) 
        window_size = self._stage.screen.get_size()
        self._grid = Grid(*self.grid_dim, self.nb_target, window_size)
        print(self._grid, self.difficulty)    # cheat mode ON


    @property
    def nb_target(self):
        return self._nb_target + self.difficulty // 2

    @property
    def grid_dim(self):
        return (dim + self.difficulty // 5 for dim in self._grid_dim)

    @property
    def lives(self):
        return self._remaining_lives

    @lives.setter
    def lives(self, value):
        self._remaining_lives = value
        if self._remaining_lives == 0:
            self._remaining_lives = self._lives
            self._stage.target = self._stage.MAIN

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        if value < 0:
            self._difficulty = 0
        else:
            self._difficulty = value

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
