#! /usr/bin/env python3

'''
Main script for the Memoz game. To play the game, run this script. For details
about the rules, see the memoz.py module.
'''

import pygame
from config import *
from utils import Stage
from memoz import *

def game():
    pygame.mixer.pre_init(44100, size=-16, buffer=512)
    icon = pygame.image.load(ICON)
    pygame.display.set_icon(icon)
    stage = Stage(STAGE_SIZE, FPS)
    pygame.display.set_caption('Memoz')


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
    game = GameScene(stage)

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

    # load sound files
    init_sounds()

    # play
    stage.play()

if __name__ == '__main__':
    game()
