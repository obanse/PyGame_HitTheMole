#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'Oliver Banse'

import time

import Colors
import pygame
from Highscore import Highscore
from Mole import Mole
from Shovel import Shovel
from pygame.locals import *
from pygame.sprite import Group


class Game():
    def __init__(self, screen):
        self.screen = screen
        self.screen.set_game(self)

        self.isfinished = False
        self.pause = False
        self.clock = pygame.time.Clock()
        self.clock.tick(30)
        pygame.time.set_timer(USEREVENT, 200)

        self.background = pygame.image.load('images/landscape.png')
        self.background = pygame.transform.scale(self.background,
                                                 self.screen.size)
        self.background_hit = pygame.Surface(self.screen.size)
        self.background_hit = self.background_hit.convert()
        self.background_hit.fill(Colors.red)

        self.music = pygame.mixer.Sound('sounds/whack.wav')
        self.muted = False

        self.mole = Mole(screen.width, screen.height, 0, 230)
        self.shovel = Shovel()

        self.count_hits = 0
        self.count_fails = 0
        self.highscore = Highscore(self.screen)
        self.player = ''


    def game_quit(self):
        self.highscore.save_highscore()
        pygame.quit()
        quit()

    # Action --> ALTER
    def game_over(self):
        self.music.fadeout(2000)

        if self.highscore.is_highscore(self.count_hits):
            self.game_highscore()

        # Assign variables
        self.isfinished = True
        # Loop
        while self.isfinished:
            # Timing
            self.clock.tick(30)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.isfinished = False

            self.screen.fill(Colors.white)
            self.screen.msg_display('GAME OVER',
                                    self.screen.width / 2,
                                    self.screen.height / 4,
                                    100)
            self.screen.msg_display(u'Maulfwürfe gefangen: ' +
                                    str(self.count_hits),
                                    self.screen.width / 2,
                                    self.screen.height / 2,
                                    40, Colors.blue)
            self.screen.button('To Mainmenu',
                               self.screen.width / 2 - 90,
                               520,
                               180,
                               40,
                               Colors.blue, Colors.bright_blue,
                               Colors.white,
                               self.game_new)

            # Redisplay
            self.screen.flip()

        self.game_menu()

    # Action --> ALTER
    def game_highscore(self):
        # Assign variables
        done = False

        # Loop
        while not done:
            self.screen.fill(Colors.light_grey)
            self.screen.msg_display('Enter name for highscore',
                                    self.screen.width / 2,
                                    self.screen.height / 4,
                                    50)
            # Timing
            self.clock.tick(30)

            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.highscore.add_highscore(self.player,
                                                     self.count_hits)
                        done = True
                    elif event.key == K_BACKSPACE:
                        self.player = self.player[:-1]
                    elif event.key == K_ESCAPE:
                        done = True
                    else:
                        self.player += event.unicode

            self.screen.button('',
                               self.screen.width / 2 - 190,
                               self.screen.height / 2 - 35,
                               400,
                               100,
                               Colors.grey, Colors.grey,
                               Colors.grey
                               )
            self.screen.button(self.player,
                               self.screen.width / 2 - 200,
                               self.screen.height / 2 - 50,
                               400,
                               100,
                               Colors.bright_blue, Colors.bright_blue,
                               Colors.white
                               )

            # Redisplay
            self.screen.flip()

    def game_continue(self):
        self.pause = False
        self.music.play(-1)

    # Action --> ALTER
    def game_pause(self):
        self.screen.fill(Colors.white)
        self.music.stop()

        # Assign variables
        self.pause = True
        # Loop
        while self.pause:
            # Timer
            clock.tick(30)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit()

            self.screen.msg_display('PAUSED',
                                    self.screen.width / 2,
                                    self.screen.height / 4,
                                    100)
            self.screen.button('Continue',
                               300, 270,
                               200, 50,
                               Colors.blue, Colors.bright_blue,
                               Colors.white,
                               self.game_continue)

            # Redisplay
            screen.flip()

    # Action --> ALTER
    def game_menu(self):
        self.screen.fill(Colors.white)

        # Assign variables
        bg = pygame.image.load('images/grass_field.jpg')
        bg = pygame.transform.scale(bg, (self.screen.size))
        button_width = 200
        button_height = 50
        menu_y_start = 200
        menu_y_gap = 20

        # Loop
        menu_isshown = True
        while menu_isshown:
            # Timer
            self.clock.tick(30)

            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    menu_isshown = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu_isshown = False

            # screen.fill(white)
            self.screen.blit(bg, (0, 0))

            self.screen.msg_display("Hit the mole!",
                                    self.screen.width / 2,
                                    self.screen.height / 5,
                                    100)

            self.screen.button('New Game',
                          self.screen.width / 2 - button_width / 2,  # x-Pos
                          menu_y_start,                              # y-Pos
                          button_width,
                          button_height,
                          Colors.green,             # inactive Color
                          Colors.bright_green,      # active Color
                          Colors.black,             # Text-Color
                          self.game_loop            # action when clicked
                          )
            self.screen.button('Highscore',
                          self.screen.width / 2 - button_width / 2,
                          menu_y_start + button_height + menu_y_gap,
                          button_width,
                          button_height,
                          Colors.blue, Colors.bright_blue,
                          Colors.white,
                          self.highscore.display_highscore
                          )
            self.screen.button('Options',
                          self.screen.width / 2 - button_width / 2,
                          menu_y_start + button_height * 2 + menu_y_gap * 2,
                          button_width,
                          button_height,
                          Colors.orange, Colors.bright_orange,
                          Colors.white
                          )
            self.screen.button('Help',
                          self.screen.width / 2 - button_width / 2,
                          menu_y_start + button_height * 3 + menu_y_gap * 3,
                          button_width,
                          button_height,
                          Colors.violett, Colors.bright_violett,
                          Colors.white
                          )
            self.screen.button('Quit Game',
                          self.screen.width / 2 - button_width / 2,
                          menu_y_start + button_height * 4 + menu_y_gap * 4,
                          button_width,
                          button_height,
                          Colors.red, Colors.bright_red,
                          Colors.white,
                          self.game_quit
                          )

            # Redisplay
            self.screen.flip()

    # Action --> ALTER
    def game_loop(self):
        self.screen.fill(Colors.white)

        # Assign variables
        sprite_group = Group()
        sprite_group.add(self.mole)
        sprite_group.add(self.shovel)
        font = pygame.font.Font(None, 25)

        self.count_hits = 0
        self.count_fails = 0
        self.music.play(-1)

        # Loop
        running = True
        while running:
            # Timing
            self.clock.tick(30)

            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_quit()
                    break
                elif event.type == MOUSEBUTTONDOWN:
                    if self.mole.hitted(pygame.mouse.get_pos()):
                        if not self.muted:
                            self.mole.cry()
                        self.count_hits += 1
                        self.screen.blit(self.background_hit, (0, 0))
                        break
                    else:
                        if self.count_fails < 2:
                            self.count_fails += 1
                        else:
                            self.game_over()
                        if not self.muted:
                            pygame.mixer.Sound('sounds/error.wav').play()
                        break
                elif event.type == USEREVENT:
                    self.mole.escape()
                    pygame.time.set_timer(USEREVENT, 1000)
                    self.screen.blit(self.background, (0, 0))
                    sprite_group.update(pygame.mouse.get_pos())
                    sprite_group.draw(self.screen.get_screen())
                    self.screen.msg_hud_left(u'Fehler: ' +
                                             str(self.count_fails),
                                             15, self.screen.height - 45,
                                             18, Colors.white)
                    self.screen.msg_hud_left(u'Maulfwürfe gefangen: ' +
                                        str(self.count_hits),
                                        15, self.screen.height - 15,
                                        18, Colors.white)
                    break
                elif event.type == KEYDOWN:
                    if event.key == K_p:
                        self.pause = True
                        self.game_pause()
                    if event.key == K_m:
                        self.muted = not self.muted
                        if self.muted:
                            self.music.stop()
                        else:
                            self.music.play(-1)

            # Redisplay
            self.screen.flip()

    def start(self):
        self.game_menu()

    def game_new(self):
        self.isfinished = False
        self.pause = False
        self.muted = False

        self.count_hits = 0
        self.count_fails = 0

        self.start()
