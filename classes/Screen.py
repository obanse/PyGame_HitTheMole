#!/usr/bin/python
# -*- encoding: utf-8 -*-
from classes import Colors

__author__ = 'Oliver Banse'

import pygame


class Screen:
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

    @staticmethod
    def flip():
        pygame.display.flip()

    def blit(self, source, destination):
        self.screen.blit(source, destination)

    def msg_display(self, text, x, y, font_size=32, font_color=Colors.black):
        font = pygame.font.Font('freesansbold.ttf', font_size)
        text_surf, text_rect = self.text_objects(text, font, font_color)
        text_rect.center = (x, y)
        self.screen.blit(text_surf, text_rect)

    def msg_hud_left(self, text, x, y, font_size=12, font_color=Colors.black):
        font = pygame.font.Font('freesansbold.ttf', font_size)
        text_surf, text_rect = self.text_objects(text, font, font_color)
        text_rect.left, text_rect.bottom = (x, y)
        self.screen.blit(text_surf, text_rect)

    def msg_hud_right(self, text, x, y, font_size=12, font_color=Colors.black):
        font = pygame.font.Font('freesansbold.ttf', font_size)
        text_surf, text_rect = self.text_objects(text, font, font_color)
        text_rect.right, text_rect.bottom = (x, y)
        self.screen.blit(text_surf, text_rect)

    @staticmethod
    def text_objects(text, font, color=Colors.black):
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

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
