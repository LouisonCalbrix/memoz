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
    pygame.mixer.pre_init(44100, size=-16, buffer=1024)
    stage = Stage(STAGE_SIZE, FPS)


    # main nav
    nav = (
        ('Play', stage.nav_link(GameScene.NAME)),
        ('Difficulty', stage.nav_link('difficulty')),
        ('Credits', stage.nav_link('credits')),
        ('Quit', stage.nav_link('quit'))
    )
    # main menu instanciation
    main_menu = MemozMenu(stage, 'Memoz', Stage.MAIN, nav=nav)

    # credits instanciation
    nav = (('Back', stage.nav_link(Stage.MAIN)), )
    menu_msg = 'Everything by:\nNoé Calbrix & Louison Calbrix'
    credits = MemozMenu(stage, 'Credits', 'credits', msg=menu_msg, nav=nav)

    # GameScene instanciation
    game = GameScene(stage, grid_dim=(rows, columns), nb_target=nb_target)

    # difficulty screen
    def change_difficulty(difficulty):
        game.difficulty = difficulty
        stage.nav_link(Stage.MAIN)()
    nav = (
        ('Easy', lambda : change_difficulty(GameScene.EASY)),
        ('Medium', lambda : change_difficulty(GameScene.MEDIUM)),
        ('Hard', lambda : change_difficulty(GameScene.HARD)),
        ('Back', stage.nav_link(Stage.MAIN))
    )
    menu_msg = 'Choose the difficulty'
    difficulty_menu = MemozMenu(stage, 'Difficulty', 'difficulty', 
                                msg=menu_msg, nav=nav)

    init_sounds()

    # play
    stage.play()

if __name__ == '__main__':
    stage_game(3, 4, 2)
