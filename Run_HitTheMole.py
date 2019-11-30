#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'Oliver Banse'

# TODO: was ist mit packages??
# TODO: Hilfe-Seite mit zurück-Button und Tasten (Bsp.: F1 - Help, P_ause, M_uted, Esc_ape)
# TODO: Optionen ausdenken, (Bsp.: Musik abschalten, Sounds abschalten, ...)
# TODO: Options Difficult-Level (Easy, Normal, Hard)
# TODO: Zufällige Zeit des Neuerscheinen des Maulwurfs
# TODO: Dimensionierung, wenn Maulwurf im Hintergrund, dann kleiner als im Vordergrund
# TODO: Überarbeitung des Maulwurfs

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


if __name__ == '__main__':
    # TODO: ist das hier notwendig?
    game.start()
