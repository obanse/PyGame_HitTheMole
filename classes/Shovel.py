#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'Oliver Banse'

import pygame
from pygame.sprite import Sprite


class Shovel(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # visualization
        self.width = 50
        self.height = 50
        self.image = pygame.image.load('images/shovel.png')
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))
        self.rect = self.image.get_rect()
        self.update(pygame.mouse.get_pos())

    def update(self, mouse_position):
        self.rect.left, self.rect.top = mouse_position
