#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
Shovel-Class: is inherited from Sprite to create a game object which is using
    a sprite for visualization
"""
__author__ = 'Oliver Banse'

import pygame
from pygame.sprite import Sprite


class Shovel(Sprite):
    # constructor
    def __init__(self):
        # call constructor from parent class
        Sprite.__init__(self)
        # visualization
        self.width = 50
        self.height = 50

        # define sprite
        self.image = pygame.image.load('images/shovel.png')
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))
        self.rect = self.image.get_rect()
        # place shovel on screen
        self.update(pygame.mouse.get_pos())

    # update position on screen
    def update(self, mouse_position):
        self.rect.left, self.rect.top = mouse_position
