#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'Oliver Banse'


# TODO:
# --> Textfeld Namen eingeben für Highscores
# -#- Hilfe-Seite mit zurück-Button und Tasten (Bsp.: F1 - Help, P_ause, M_uted, Esc_ape)
# -#- Optionen ausdenken, (Bsp.: Musik abschalten, Sounds abschalten, ...)
# -#- Überarbeitung des Maulwurfs
# -#- Options Difficult-Level (Easy, Normal, Hard)
# --> Zufällige Zeit des Neuerscheinen des Maulwurfs
# --> Dimensionierung, wenn Maulwurf im Hintergrund, dann kleiner als im Vordergrund

# IDEA
# Import and Initialization
import pygame
from Game import Game
from Screen import Screen
from pygame.locals import *
pygame.init()

# Display configuration
screen = Screen('Hit the Mole!', 800, 600)
# Entities
game = Game(screen)

# Run Game
game.start()
