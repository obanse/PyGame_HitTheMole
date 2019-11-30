#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'Oliver Banse'

import pygame
import Colors
import json
from pygame.locals import *
from operator import itemgetter



# TODO: Highscore umstruckturieren! TextInput
# --> check_highscore() --> if highscore then
# --> get_player_name() --> return name
# --> add_highscore(name, num_hits)
# --> on_quit --> save_highscore()

class Highscore():
    def __init__(self, screen):
        self.screen = screen
        self.highscore = self.load_highscore()

    def load_highscore(self):
        try:
            with open('highscore.json', 'r') as file:
                self.highscore = json.load(file)
        except FileNotFoundError:
            return []
        return sorted(self.highscore, key=itemgetter(1), reverse=True)

    def save_highscore(self):
        with open('highscore.json', 'w') as file:
            json.dump(self.highscore, file)

    def is_highscore(self, num_hits):
        self.highscore = self.load_highscore()
        if len(self.highscore) < 10:
            return True
        elif self.highscore[len(self.highscore) - 1][1] < num_hits:
            return True
        return False

    def add_highscore(self, name, num_hits):
        self.highscore = self.load_highscore()

        if len(self.highscore) < 10:
            self.highscore.append([name, num_hits])
        elif self.highscore[len(self.highscore) - 1][1] < num_hits:
            self.highscore.pop(len(self.highscore) - 1)
            self.highscore.append([name, num_hits])

        self.save_highscore()

    def display_highscore(self):
        font = pygame.font.Font('freesansbold.ttf', 20)
        self.highscore = self.load_highscore()

        while True:
            self.screen.fill((255,255,255))
            # Display the high-scores.
            self.screen.msg_display('Highscore',
                                    self.screen.width/2,
                                    self.screen.height/5,
                                    100)

            for y, (hi_name, hi_score) in enumerate(self.highscore):
                TextSurf, TextRect = self.screen.text_objects(
                    f'{hi_name} - {hi_score} Pkt.', font, Colors.blue)
                TextRect.left, TextRect.top = ((330, y * 30 + 200))
                self.screen.blit(TextSurf, TextRect)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.screen.game.game_menu()

            self.screen.button('Go Back',
                               self.screen.width / 2 - 90, 520,
                               180, 40,
                               Colors.blue, Colors.bright_blue,
                               Colors.white,
                               self.screen.game.game_menu)

            self.screen.flip()
            self.screen.game.clock.tick(30)
