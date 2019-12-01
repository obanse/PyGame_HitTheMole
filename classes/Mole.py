#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
Mole-Class: inherited from Sprite, used to create a mole object and add a
    sprite for visualization in game world
"""
__author__ = 'Oliver Banse'

import random

import pygame
from pygame.sprite import Sprite


class Mole(Sprite):
    # constructor
    def __init__(self, screen_width, screen_height,
                 threshold_left=0, threshold_top=0):
        # call constructor from parent class
        Sprite.__init__(self)
        # visualization
        self.width = 60
        self.height = 96

        # define sprite
        self.image = pygame.image.load('images/mole.png')
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))
        # define the hit-box
        self.rect = self.image.get_rect()
        # define sound when mole is hitted
        self.sound = pygame.mixer.Sound('sounds/mole_ow.wav')
        # set screen range
        self.screen_width = screen_width
        self.screen_height = screen_height
        # set range where the mole can be placed on self painted game world
        self.threshold_left = threshold_left
        self.threshold_top = threshold_top
        # initialy place mole by setting position data
        self.__place()

    # set new randomly position data depending on range settings
    def __place(self):
        self.rect.left = random.randint(self.threshold_left,
                                        self.screen_width - self.width)
        self.rect.top = random.randint(self.threshold_top,
                                       self.screen_height - self.height)

    # when mole is fleeing a new position will be set
    def escape(self):
        self.__place()

    # play sound when mole is crying
    def cry(self):
        self.sound.play()

    # check if param 'pos' is within the hit-box
    def hitted(self, pos):
        return self.rect.collidepoint(pos)
