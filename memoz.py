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


# sounds to be used by following Scene subclasses
ui_sound_ok = 0
ui_sound_bad = 0
ui_sound_menu = 0
def init_sounds():
    global ui_sound_ok
    global ui_sound_bad
    global ui_sound_menu
    ui_sound_ok = pygame.mixer.Sound(SOUND_OK)
    ui_sound_bad = pygame.mixer.Sound(SOUND_BAD)
    ui_sound_menu = pygame.mixer.Sound(SOUND_MENU)


class GameScene(utils.Scene):
    '''
    GameScene is the class that encapsulate the game logic. It allows the player
    to interact with a game's grid and display that grid onscreen.
    '''
    # height of the time relatively to the height of the whole screen (in %)
    TIMER_REL_HEIGHT = 2
    TIMER_ABS_HEIGHT = 0                  # to be initialized 
    NAME = 'game'                         # name of the GameScene for the Stage
    EASY = {
        '_grid_dim': (3, 3),
        '_nb_target': 1,
        '_time': 3.5,
        '_tries': 5,
    }
    MEDIUM = {
        '_grid_dim': (4, 3),
        '_nb_target': 2,
        '_time': 2.5,
        '_tries': 3,
    }
    HARD = {
        '_grid_dim': (7, 5),
        '_nb_target': 3,
        '_time': 1.8,
        '_tries': 2,
    }

    def __init__(self, stage, grid_dim=(2, 2), nb_target=2, time=2,
                 total_tries=3, lives=3):
        super().__init__(stage, self.NAME)
        self._time = time           # time tiles will be revealed at the beginning
        self._grid_dim = grid_dim   # size of Grid instances 
        self._nb_target = nb_target
        self._tries = total_tries   # number of tries before game over
        self._lives = lives         # number of game that can be lost before back to menu
        self._level = 0
        self._remaining_lives = lives
        self._game_over = True
        type(self).TIMER_ABS_HEIGHT = self.TIMER_REL_HEIGHT * STAGE_SIZE[1] // 100

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
                            ui_sound_bad.play()
                            self._remaining_tries -= 1
                        else:
                            ui_sound_ok.play()

                        if not self._remaining_tries:              # lost game
                            self.level -= 1
                            self._game_over = True               
                            self.lives -= 1
                        elif self._grid.points == self.nb_target:  # won game
                            self.level += 1
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
        font = pygame.font.Font(FONT_PRIM, FONT_SIZE_2)
        txt_surf = font.render(str(self._remaining_tries), True, COLOR_ORANGE)
        self._stage.screen.blit(txt_surf, (0,0))

    def draw_timer(self):
        '''
        Draw onscreen a representation of the time remaining during which
        tiles are all revealed.
        '''
        if self._timer:
            width = int((self._timer / (self._time * FPS)) * STAGE_SIZE[0])
            rect = pygame.Rect(0, STAGE_SIZE[1]-self.TIMER_ABS_HEIGHT, 
                               width, self.TIMER_ABS_HEIGHT)
            pygame.draw.rect(self._stage.screen, COLOR_ORANGE, rect)
    
    # Own functionnalities

    def start_game(self):
        '''
        Instanciate Grid, initialize _remaining_tries and timer.
        '''
        self._game_over = False
        self._remaining_tries = self._tries   # current number of tries (to be decreased)
        self._timer = self._time * FPS        # timer (to be decreased) 
        self._grid = Grid(*self.grid_dim, self.nb_target, STAGE_SIZE)
        print(self._grid, self.level)         # cheat mode ON


    @property
    def nb_target(self):
        return self._nb_target + self.level // 2

    @property
    def grid_dim(self):
        return (dim + self.level // 5 for dim in self._grid_dim)

    @property
    def lives(self):
        return self._remaining_lives

    @lives.setter
    def lives(self, value):
        self._remaining_lives = value
        if self._remaining_lives == 0:
            self._remaining_lives = self._lives
            self.level = 0
            self._stage.target = self._stage.MAIN

    @property
    def difficulty(self):
        diff_settings = { '_grid_dim', '_nb_target', '_time', '_total_tries' }
        dif = { name: val for name, val in self.__dict__ if name in diff_settings }
        return dif

    @difficulty.setter
    def difficulty(self, new_difficulty):
        for name, value in new_difficulty.items():
            setattr(self, name, value)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        if value < 0:
            self._level = 0
        else:
            self._level = value


class MemozMenu(utils.Menu):
    '''
    A Menu kind of Scene for memoz. Using this kind of Menu enforces the Memoz 
    "look" and allows changes of look here to impact all the Menu created with
    this class.
    '''

    # margins are indicated in pixels rmargins are relative to the element of the
    # menu they're related to.
    TITLE_MARGIN = 50
    TITLE_RMARGIN = 1.5
    MSG_RMARGIN = 1.2
    NAV_INFLATE = (1.7, 0.9)
    NAV_RMARGIN = 1.3

    def __init__(self, stage, title, name, nav=None, msg=None):
        '''
        Initialize MemozMenu instance with a title that will be displayed using 
        the FONT_TITLE. Options include:
            - Buttons can be added directly at instanciation by giving nav a list
              of tuples (button_name, action), these are preferably for navigating 
              to other Scenes. 
            - msg can contain a string that will be displayed using FONT_PRIM
        '''
        surf = pygame.Surface(STAGE_SIZE)
        surf.fill(COLOR_BLACK)


        pos_y = self.draw_title(surf, title)
        # writes down msg if any
        if msg:
            pos_y = self.draw_msg(surf, msg, pos_y)

        # super initializer needs to be called before adding buttons
        super().__init__(stage, name, img=surf)

        if nav:
            self.add_nav(nav, pos_y)

    def draw_title(self, surf, title):
        '''
        Draw title of this Menu on surf using FONT_TITLE and draw a square 
        around each letter. A pos_y is returned from where it is safe to draw 
        other elements.
        '''
        width_title = round(0.8 * STAGE_SIZE[0])           # title as wide as 80% of screen
        self.pos_x = (STAGE_SIZE[0] - width_title) // 2
        pos_y = self.TITLE_MARGIN
        square_size = 0.9 * width_title // len(title)      # title is 90% squares 10% margin
        margin_size = (width_title - len(title) * square_size) // (len(title) - 1)
        mem_font = pygame.font.Font(FONT_TITLE, round(0.8*square_size))
        for i, letter in enumerate(title):
            x_rect = self.pos_x + (square_size+margin_size)*i
            rect = pygame.Rect((x_rect, pos_y),
                               (square_size, square_size))
            pygame.draw.rect(surf, COLOR_BLUE_1, rect)
            color = COLOR_BLACK
            if letter == 'o':
                color = COLOR_YELLOW
            letter_surf = mem_font.render(letter, True, color)
            x_letter = x_rect + (square_size-letter_surf.get_width()) // 2
            y_letter = pos_y + (square_size-letter_surf.get_height()) // 2
            surf.blit(letter_surf, (x_letter, y_letter))
        return pos_y + self.TITLE_RMARGIN * square_size

    def draw_msg(self, surf, msg, pos_y):
        '''
        Write down msg on surf starting from pos_y. It returns a pos_y from 
        where it is safe to draw other elements.
        '''
        msg_font = pygame.font.Font(FONT_PRIM, FONT_SIZE_2)
        for line in msg.split('\n'):
            line_surf = msg_font.render(line, True, COLOR_YELLOW)
            pos_x = (STAGE_SIZE[0] - line_surf.get_width()) // 2
            surf.blit(line_surf, (pos_x, pos_y))
            pos_y += round(msg_font.get_linesize() * self.MSG_RMARGIN)
        return pos_y

    def add_nav(self, nav, pos_y):
        '''
        Add several buttons (typically navigation buttons) and draw them on
        the widget surface starting from pos_y.
        '''
        # determine buttons' size depending on the longest name
        font = pygame.font.Font(FONT_PRIM, FONT_SIZE_2)
        msize = max((font.size(name) for (name, _) in nav), key=lambda x_y: x_y[0])
        # inflate
        msize = tuple(round(dim * factor) for dim, factor in zip(msize, self.NAV_INFLATE))
        b_width, b_height = msize
        pos_x = (STAGE_SIZE[0] - b_width) // 2
        height_avail = STAGE_SIZE[1] - pos_y
        rel_y = (height_avail - b_height * ((1 + self.NAV_RMARGIN) * len(nav) - self.NAV_RMARGIN)) // 2
        pos_y = pos_y + rel_y

        def ring_and_action(action):
            def func():
                ui_sound_menu.play()
                action()
            return func
        for name, action in nav:
            real_action = ring_and_action(action)
            button = utils.Button.fromstring(name, real_action, fontfile=FONT_PRIM,
                                             size_px=FONT_SIZE_2, font_color=COLOR_BLACK,
                                             bg_color=COLOR_BLUE_1, size=msize)
            super().add_button_at(button, (pos_x, pos_y))
            pos_y += b_height * self.NAV_RMARGIN
