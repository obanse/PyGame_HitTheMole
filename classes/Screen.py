#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
Screen-Class: creates a screen object where the game world, menus, text, etc.
    can by displayed
"""
__author__ = 'Oliver Banse'

import pygame

from classes import Colors

pygame.init()


class Screen:
    # constructor
    def __init__(self, title, width, height):
        # set title
        self.title = title
        pygame.display.set_caption(self.title)
        # set screen dimension
        self.width = width
        self.height = height
        self.size = (width, height)     # ...also as tupel
        self.screen = pygame.display.set_mode(self.size)
        self.game = None                # initialy game object will be None

    # set the game object
    def set_game(self, game):
        self.game = game

    # return the screen
    def get_screen(self):
        return self.screen

    # fill screen
    def fill(self, color):
        self.screen.fill(color)

    # display a pygame surface
    def blit(self, source, destination):
        self.screen.blit(source, destination)

    # define and set a message on screen
    def msg_display(self, text, x, y, font_size=32, font_color=Colors.black):
        font = pygame.font.Font('freesansbold.ttf', font_size)
        text_surf, text_rect = self.text_objects(text, font, font_color)
        text_rect.center = (x, y)
        self.screen.blit(text_surf, text_rect)

    # define and set a message on screen
    def msg_hud_left(self, text, x, y, font_size=12, font_color=Colors.black):
        font = pygame.font.Font('freesansbold.ttf', font_size)
        text_surf, text_rect = self.text_objects(text, font, font_color)
        text_rect.left, text_rect.bottom = (x, y)
        self.screen.blit(text_surf, text_rect)

    # define and set a message on screen
    def msg_hud_right(self, text, x, y, font_size=12, font_color=Colors.black):
        font = pygame.font.Font('freesansbold.ttf', font_size)
        text_surf, text_rect = self.text_objects(text, font, font_color)
        text_rect.right, text_rect.bottom = (x, y)
        self.screen.blit(text_surf, text_rect)

    # define and set a button on screen
    def button(self, text, x, y, width, height, inactive_color,
               active_color, text_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.screen, active_color,
                             (x, y, width, height))
            if click[0] and action is not None:
                action()
        else:
            pygame.draw.rect(self.screen, inactive_color,
                             (x, y, width, height))

        font = pygame.font.Font('freesansbold.ttf', 20)
        text_surf, text_rect = self.text_objects(text, font, text_color)
        text_rect.center = ((x + (width / 2)), (y + (height / 2)))
        self.screen.blit(text_surf, text_rect)

    # refresh/redisplay
    @staticmethod
    def flip():
        pygame.display.flip()

    # returns pygame surface
    @staticmethod
    def text_objects(text, font, color=Colors.black):
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()
