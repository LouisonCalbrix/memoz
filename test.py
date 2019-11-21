#! /usr/bin/env python3

# test script for the game of memoz
# this script's sole purpose is to test the different components of the game
# to ensure its proper functionning. 

import pygame
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
    screen = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()
    fps = 20
    # every 50 frame target_tile3 and wrong_tile3 are flipped
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

if __name__ == '__main__':
    tile_display()
