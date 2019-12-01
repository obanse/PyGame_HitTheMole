#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'Oliver Banse'


# IDEA
# Import and Initialization
import pygame

from classes.Game import Game
from classes.Screen import Screen

pygame.init()

# Display configuration
screen = Screen('Hit the Mole!', 800, 600)
# Entities
game = Game(screen)
# Run Game
game.start()


# if __name__ == '__main__':
#     game.start()
