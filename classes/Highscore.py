#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
Highscore-Class: creates a highscore-object with several methods within to
    manage highscore. For example saving, loading and displaying the
    highscores
"""
__author__ = 'Oliver Banse'

import json
from operator import itemgetter

from classes import Colors
import pygame
from pygame.locals import *


class Highscore:
    # constructor
    def __init__(self, screen):
        # set screen where it should be displayed
        self.screen = screen
        # load highscores
        self.highscore = self.load_highscore()

    # load highscores from json-file
    def load_highscore(self):
        try:
            with open('highscore.json', 'r') as file:
                self.highscore = json.load(file)
        except FileNotFoundError:
            return []
        return sorted(self.highscore, key=itemgetter(1), reverse=True)

    # save highscores to json-file
    def save_highscore(self):
        with open('highscore.json', 'w') as file:
            json.dump(self.highscore, file)

    # method to check if points are enough for highscore
    def is_highscore(self, points):
        self.highscore = self.load_highscore()
        if len(self.highscore) < 10:
            return True
        elif self.highscore[len(self.highscore) - 1][1] < points:
            return True
        return False

    # add name and points to highscore
    def add_highscore(self, name, points):
        self.highscore = self.load_highscore()

        if len(self.highscore) < 10:
            self.highscore.append([name, points])
        elif self.highscore[len(self.highscore) - 1][1] < points:
            self.highscore.pop(len(self.highscore) - 1)
            self.highscore.append([name, points])

        self.save_highscore()

    # show highscore screen
    def display_highscore(self):
        font = pygame.font.Font('freesansbold.ttf', 20)
        # load highscores again to get a new sorted array
        self.highscore = self.load_highscore()

        # Display the high-scores.
        while True:
            self.screen.fill(Colors.white)
            # add headline
            self.screen.msg_display('Highscore',
                                    self.screen.width / 2,
                                    self.screen.height / 5,
                                    100)
            # inkremented variable for displaying the rank
            count_rank = 1
            # display every rank from highscore
            for y, (hi_name, hi_score) in enumerate(self.highscore):
                text_surf, text_rect = self.screen.text_objects(
                    f'{count_rank}. {hi_name} - {hi_score} Pkt.',
                    font, Colors.blue)
                text_rect.left, text_rect.top = (self.screen.width / 3,
                                                 y * 30 + 200)
                self.screen.blit(text_surf, text_rect)
                count_rank += 1

            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.screen.game.show_mainmenu()

            # add go_back-Button to show main menu
            self.screen.button('Go Back',
                               580, 520,
                               180, 40,
                               Colors.blue, Colors.bright_blue,
                               Colors.white,
                               self.screen.game.show_mainmenu)
            # Redisplay
            self.screen.flip()
            self.screen.game.clock.tick(30)
