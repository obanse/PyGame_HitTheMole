#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'Oliver Banse'

import Colors
import pygame
from pygame.locals import *

# -> define some colors
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
orange = (255,127,0)
violett = (127,42,255)
bright_red = (255,0,0)
bright_green = (0,255,0)
bright_blue = (0,0,255)
bright_orange = (254,169,42)
bright_violett = (127,85,255)


class Screen():
    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)
        self.game = None
        pygame.display.set_caption(self.title)

    def set_game(self, game):
        self.game = game

    def get_screen(self):
        return self.screen

    def fill(self, color):
        self.screen.fill(color)

    def flip(self):
        pygame.display.flip()

    def blit(self, source, destination):
        self.screen.blit(source, destination)

    def msg_display(self, text, x, y, font_size=32, font_color=Colors.black):
        font = pygame.font.Font('freesansbold.ttf', font_size)
        TextSurf, TextRect = self.text_objects(text, font, font_color)
        TextRect.center = ((x, y))
        self.screen.blit(TextSurf, TextRect)

    def msg_display(self, text, x, y, font_size=32, font_color=Colors.black):
        font = pygame.font.Font('freesansbold.ttf', font_size)
        TextSurf, TextRect = self.text_objects(text, font, font_color)
        TextRect.center = ((x, y))
        self.screen.blit(TextSurf, TextRect)

    def msg_hud_left(self, text, x, y, font_size=12, font_color=Colors.black):
        font = pygame.font.Font('freesansbold.ttf', font_size)
        TextSurf, TextRect = self.text_objects(text, font, font_color)
        TextRect.left, TextRect.bottom = ((x, y))
        self.screen.blit(TextSurf, TextRect)

    def msg_hud_right(self, text, x, y, font_size=12, font_color=Colors.black):
        font = pygame.font.Font('freesansbold.ttf', font_size)
        TextSurf, TextRect = self.text_objects(text, font, font_color)
        TextRect.right, TextRect.bottom = ((x, y))
        self.screen.blit(TextSurf, TextRect)

    def text_objects(self, text, font, color=Colors.black):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def button(self, text, x, y, width, height, inactive_color,
                   active_color, text_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.screen, active_color,
                             (x, y, width, height))
            if click[0] and action != None:
                action()
        else:
            pygame.draw.rect(self.screen, inactive_color,
                             (x, y, width, height))

        font = pygame.font.Font('freesansbold.ttf', 20)
        textSurf, textRect = self.text_objects(text, font, text_color)
        textRect.center = ((x + (width / 2)), (y + (height / 2)))
        self.screen.blit(textSurf, textRect)


