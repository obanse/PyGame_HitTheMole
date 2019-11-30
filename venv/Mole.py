#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'Oliver Banse'

import pygame
import random
from pygame.sprite import Sprite


class Mole(Sprite):
    def __init__(self, screen_width, screen_height, threshold_left=0, threshold_top=0):
        Sprite.__init__(self)
        # visualization
        self.width = 60
        self.height = 96
        self.image = pygame.image.load('images/mole.png')
        self.image = pygame.transform.scale(self.image,
                                    (self.width, self.height))
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound('sounds/mole_ow.wav')
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.threshold_left = threshold_left
        self.threshold_top = threshold_top
        self.__place()

    def __place(self):
        self.rect.left = random.randint(self.threshold_left,
                                        self.screen_width - self.width)
        self.rect.top = random.randint(self.threshold_top,
                                       self.screen_height - self.height)

    def escape(self):
        self.__place()

    def cry(self):
        self.sound.play()

    def hitted(self, pos):
        return self.rect.collidepoint(pos)