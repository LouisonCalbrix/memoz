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

    main_img = pygame.Surface(stage.screen.get_size())
    main_img.fill((0, 0, 0))

    # MEMOZ with a blue square around each letter
    width_memoz = round(0.8 * STAGE_SIZE[0])
    pos_x = (STAGE_SIZE[0] - width_memoz) // 2
    pos_y = 50
    square_size = 100
    margin_size = (width_memoz - len('MEMOZ') * square_size) // (len('MEMOZ') - 1)
    mem_font = pygame.font.Font(None, 100)
    for i, letter in enumerate('MEMOZ'):
        x_rect = pos_x + (square_size+margin_size)*i
        rect = pygame.Rect((x_rect, pos_y),
                           (square_size, square_size))
        pygame.draw.rect(main_img, COLOR_BLUE_1, rect)
        color = COLOR_BLACK
        if letter == 'O':
            color = COLOR_YELLOW
        letter_surf = mem_font.render(letter, True, color)
        x_letter = x_rect + (square_size-letter_surf.get_width()) // 2
        y_letter = pos_y + (square_size-letter_surf.get_height()) // 2
        main_img.blit(letter_surf, (x_letter, y_letter))

    # main menu instanciation
    main_menu = Menu(stage, img=main_img)
    # buttons for main menu
    # button 1: play
    play_button = Button.fromstring('Play', action=stage.nav_link('game'), 
                                    size_px=52, size=(150, 50), 
                                    bg_color=COLOR_BLUE_1, font_color=COLOR_BLACK)
    main_menu.add_button_at(play_button, (pos_x, 350))
    # button 2: quit
    quit_button = Button.fromstring('Quit', action=stage.nav_link('quit'),
                                    size_px=52, size=(150, 50), 
                                    bg_color=COLOR_BLUE_1, font_color=COLOR_BLACK)
    main_menu.add_button_at(quit_button, (pos_x, 450))

    # add main_menu Scene to the Stage as MAIN
    stage[Stage.MAIN] = main_menu

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
