#! /usr/bin/env python3

# test script for the game of memoz
# this script's sole purpose is to test the different components of the game
# to ensure its proper functionning. 

import pygame
from config import *
from utils import Stage, Menu, Button
from memoz import *

def tile_display():
    # target_tile1 is revealed and target_tile2 is hidden
    # the third one is flipped on a regular basis
    target_tile1 = Tile(True, True)
    target_tile2 = Tile(True, False)
    target_tile3 = Tile(True, False)
    # wrong_tile1 is revealed and wrong_tile2 is hidden
    # the third one is flipped on a regular basis
    wrong_tile1 = Tile(False, True)
    wrong_tile2 = Tile(False, False)
    wrong_tile3 = Tile(False, False)

    tiles = [
        target_tile1,
        target_tile2,
        target_tile3,
        wrong_tile1,
        wrong_tile2,
        wrong_tile3
    ]
    # pygame init
    pygame.init()
    screen = pygame.display.set_mode((150, 100))
    clock = pygame.time.Clock()
    fps = 20
    # every 30 frame target_tile3 and wrong_tile3 are flipped
    frame_count = 0
    flip_frequency = 30
    while True:
        clock.tick(fps)
        frame_count += 1
        if frame_count == flip_frequency:
            target_tile3.flip()
            wrong_tile3.flip()
            frame_count = 0
        for i, tile in enumerate(tiles):
            x, y = (i % 3) * 50, (i // 3) * 50
            tile.draw_at(screen, (x, y))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        pygame.display.flip()

def grid_display(rows, columns, nb_targets):
    window_size = (450, 700)
    grid = Grid(rows, columns, nb_targets, window_size)

    # pygame init
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()
    fps = 20
    # after 100 frames all the tiles of the grid are hidden
    frame_count = 100
    while True:
        if frame_count != 0:
            frame_count -= 1
        elif frame_count == 0:
            grid.hide_all()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print('mouse on tile: {}'.format(grid.tile_at(mouse_pos)))
            
        grid.draw(screen)
        pygame.display.flip()
        clock.tick(fps)

def stage_game(rows, columns, nb_target):
    fps = 30
    stage = Stage(STAGE_SIZE, fps)

    class MemozMenu(Menu):
        def __init__(self, title):
            surf = pygame.Surface(stage.screen.get_size())
            surf.fill(COLOR_BLACK)

            # Memoz with a blue square around each letter
            width_title = round(0.8 * STAGE_SIZE[0])
            self.pos_x = (STAGE_SIZE[0] - width_title) // 2
            pos_y = 50
            square_size = 0.9 * width_title // len(title)
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
            super().__init__(stage, img=surf)

    # main menu instanciation
    main_menu = MemozMenu('Memoz')
    # buttons for main menu
    button_y = 350
    button_x = main_menu.pos_x
    button_margin = 20
    button_size = (150, 50)
    button_ft_size = 52
    navbuttons_txt = (('Play', 'game'),
                      ('Credits', 'credits'),
                      ('Quit', 'quit'))
    for i, (text, target) in enumerate(navbuttons_txt):
        button = Button.fromstring(text, action=stage.nav_link(target),
                                   size_px=button_ft_size, size=button_size,
                                   bg_color=COLOR_BLUE_1, font_color=COLOR_BLACK)
        main_menu.add_button_at(button, (button_x, button_y))
        button_y += button_margin + button_size[1]

    # add main_menu Scene to the Stage as MAIN
    stage[Stage.MAIN] = main_menu

    # credits instanciation
    credits = MemozMenu('Credits')
    text_surf = pygame.font.Font(None, 55).render('Everything by:', True, COLOR_BLUE_2)
    credits.img.blit(text_surf, (200, 250))
    text_surf = pygame.font.Font(None, 55).render('Noé Calbrix & Louison Calbrix', True, COLOR_YELLOW)
    credits.img.blit(text_surf, (50, 300))
    button = Button.fromstring('Back', action=stage.nav_link(Stage.MAIN),
                               size_px=button_ft_size, size=button_size,
                               bg_color=COLOR_BLUE_1, font_color=COLOR_BLACK)
    credits.add_button_at(button, (button_x, button_y))
    stage['credits'] = credits

    # GameScene instanciation
    time = 2 * fps
    game = GameScene(stage, grid_dim=(rows, columns), nb_target=nb_target,
                     time=time)

    # add game Scene to the Stage as 'game'
    stage['game'] = game

    # play
    stage.play()

if __name__ == '__main__':
    stage_game(3, 4, 2)
