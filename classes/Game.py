#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
Game-Class: initializes the whole game by defining game objects, variables,
    game-logic, etc.
"""
__author__ = 'Oliver Banse'

import pygame
from pygame.locals import *
from pygame.sprite import Group

from classes import Colors
from classes.Highscore import Highscore
from classes.Mole import Mole
from classes.Shovel import Shovel

pygame.init()


class Game:
    # constructor
    def __init__(self, screen):
        self.screen = screen
        # set game-object on screen-object
        self.screen.set_game(self)
        # game difficult levels
        self.levels = dict({1: 'easy', 2: 'normal', 3: 'hard'})
        # default difficult level and set timer the mole escapes
        self.game_level = 2
        self.escape_timer = 1000

        # bool variables for checking shown menus or game states
        self.isfinished = False
        self.help_isshown = False
        self.options_isshown = False
        self.pause = False
        self.muted = False

        # set clock timing / fps
        self.clock = pygame.time.Clock()
        self.clock.tick(30)
        pygame.time.set_timer(USEREVENT, 200)

        # set self painted background image for the game
        self.background_game = pygame.image.load('images/landscape.png')
        self.background_game = pygame.transform.scale(self.background_game,
                                                      self.screen.size)
        # set background image for main menu
        self.background_menu = pygame.image.load('images/grass_field.jpg')
        self.background_menu = pygame.transform.scale(self.background_menu,
                                                      self.screen.size)
        # set background when mole was hitted
        self.background_hit = pygame.Surface(self.screen.size)
        self.background_hit = self.background_hit.convert()
        self.background_hit.fill(Colors.red)

        # set game music
        self.music = pygame.mixer.Sound('sounds/whack.wav')

        # set and initialize game objects
        self.mole = Mole(screen.width, screen.height, 0, 230)
        self.shovel = Shovel()

        # initialize game variables
        self.points = 0
        self.count_fails = 0
        self.highscore = Highscore(self.screen)
        # set player name to empty string
        self.player = ''

    # game shutdown procedure
    def game_quit(self):
        # save highscores
        self.highscore.save_highscore()
        print('Highscore saved. Game End!')
        pygame.quit()
        quit()

    # show game over display
    def game_over(self):
        # reduce and stop music playing
        self.music.fadeout(2000)

        # check highscore
        if self.highscore.is_highscore(self.points):
            # if highscore is good open highscore-dialog
            self.game_highscore()

        # Assign variables - is game finished?
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

            # fill background with white
            self.screen.fill(Colors.white)
            # add headline to screen
            self.screen.msg_display('GAME OVER',
                                    self.screen.width / 2,
                                    self.screen.height / 4,
                                    100)
            # add points to screen
            self.screen.msg_display(u'Punkte: ' +
                                    str(self.points),
                                    self.screen.width / 2,
                                    self.screen.height / 2,
                                    40, Colors.blue)
            # add button to go back to main menu
            self.screen.button('Go To Main',
                               self.screen.width / 2 - 90,
                               520,
                               180,
                               40,
                               Colors.blue, Colors.bright_blue,
                               Colors.white,
                               self.show_mainmenu)

            # Redisplay
            self.screen.flip()
        # when game is not finished anymore show main menu
        self.show_mainmenu()

    # show player input name window
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
                                                     self.points)
                        done = True
                    elif event.key == K_BACKSPACE:
                        self.player = self.player[:-1]
                    elif event.key == K_ESCAPE:
                        done = True
                    else:
                        self.player += event.unicode

            # add button/rectangle as shadow effect
            self.screen.button('',
                               self.screen.width / 2 - 190,
                               self.screen.height / 2 - 35,
                               400,
                               100,
                               Colors.grey, Colors.grey,
                               Colors.grey
                               )
            # add button as input-box where the player inputs his name
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

    # show options menu
    def show_options(self):
        # Assign variables
        button_width = 250
        button_height = 50
        menu_y_start = 200
        menu_y_gap = 20
        self.options_isshown = True

        # Loop
        while self.options_isshown:
            # fill background with white color
            self.screen.fill(Colors.white)
            # add headline
            self.screen.msg_display('Options',
                                    self.screen.width / 2,
                                    self.screen.height / 5,
                                    100)

            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit_options()
                    elif event.key == K_s:
                        self.toogle_muted()
                    elif event.key == K_g:
                        self.toggle_game_level()
                elif event.type == MOUSEBUTTONUP:
                    # get mouse coordinates
                    mouse = pygame.mouse.get_pos()
                    # Muted-Button clicked?
                    if (self.screen.width / 2) - (button_width / 2) \
                            + button_width > mouse[0] > \
                            (self.screen.width / 2) - (button_width / 2) \
                            and (menu_y_start + button_height) > mouse[1] > \
                            menu_y_start:
                        self.toogle_muted()
                    # Game_level-Button clicked?
                    if (self.screen.width / 2) - (button_width / 2) \
                            + button_width > mouse[0] > \
                            (self.screen.width / 2) - (button_width / 2) \
                            and (menu_y_start + button_height * 2 + menu_y_gap) \
                            > mouse[1] > \
                            menu_y_start + button_height + menu_y_gap:
                        self.toggle_game_level()

            # set text and button-colors for muted-Button
            if self.muted:
                btn_color_active = Colors.bright_red
                btn_color_inactive = Colors.red
                btn_muted_text = '[S]ounds: off'
            else:
                btn_color_active = Colors.bright_green
                btn_color_inactive = Colors.green
                btn_muted_text = '[S]ounds: on'
            # set text for game_level-Button
            btn_game_level_text = self.levels.get(self.game_level)

            # add muted-Button
            self.screen.button(btn_muted_text,
                               self.screen.width / 2 - button_width / 2,
                               menu_y_start,
                               button_width, button_height,
                               btn_color_inactive,  # inactive Color
                               btn_color_active,  # active Color
                               Colors.black  # Text-Color
                               )

            # add game_level-Button
            self.screen.button(f'Game-Level: {btn_game_level_text}',
                               self.screen.width / 2 - button_width / 2,
                               menu_y_start + button_height + menu_y_gap,
                               button_width, button_height,
                               Colors.blue, Colors.bright_blue,
                               Colors.white
                               )

            # add go_back-Button
            self.screen.button('Go Back',
                               580, 520,
                               180, 40,
                               Colors.blue, Colors.bright_blue,
                               Colors.white,
                               self.exit_options)

            self.screen.flip()
            self.screen.game.clock.tick(30)
        # when options menu will be exited -> show main menu
        self.show_mainmenu()

    # toggle the game level
    def toggle_game_level(self):
        if self.game_level == 1:
            self.game_level = 2
        elif self.game_level == 2:
            self.game_level = 3
        elif self.game_level == 3:
            self.game_level = 1
        self.set_level_settings()

    # set level difficult values depending on game level
    def set_level_settings(self):
        if self.game_level == 1:
            self.escape_timer = 2000
        elif self.game_level == 2:
            self.escape_timer = 1000
        elif self.game_level == 3:
            self.escape_timer = 800
        # debugging output when changing game level
        print(f'Game-Level: {self.levels.get(self.game_level)}, '
              f'Escape-Timer: {self.escape_timer}')

    # toggle sounds to mute / unmute
    def toogle_muted(self):
        if self.muted:
            self.muted = False
            print("Sounds unmuted!")
        else:
            self.muted = True
            print("Sounds muted!")


    # exit options menu
    def exit_options(self):
        self.options_isshown = False
        self.show_mainmenu()

    # show help menu
    def show_help(self):
        # Assign variables
        top_anchor = 250
        top_anchor_gap = 40
        self.help_isshown = True

        # Loop
        while self.help_isshown:
            # Timing
            # fill background with color white
            self.screen.fill(Colors.white)
            # add headline
            self.screen.msg_display('Help',
                                    self.screen.width / 2,
                                    self.screen.height / 5,
                                    100)
            # add text to display keyboard functions
            self.screen.msg_display('[P] --> Pause, take a break',
                                    self.screen.width / 2,
                                    top_anchor,
                                    20)
            self.screen.msg_display('[M] --> Mute sounds',
                                    self.screen.width / 2,
                                    top_anchor + top_anchor_gap,
                                    20)
            self.screen.msg_display('[ESC] --> Go Back or Quit Game',
                                    self.screen.width / 2,
                                    top_anchor + top_anchor_gap * 2,
                                    20)

            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit_help()

            # add go_back-Button
            self.screen.button('Go Back',
                               580, 520,
                               180, 40,
                               Colors.blue, Colors.bright_blue,
                               Colors.white,
                               self.exit_help)

            self.screen.flip()
            self.screen.game.clock.tick(30)
        # when options menu will be exited -> show main menu
        self.show_mainmenu()

    # exit help menu
    def exit_help(self):
        self.help_isshown = False
        self.show_mainmenu()

    # pause the game and show pause screen
    def game_pause(self):
        # fill background screen with color white
        self.screen.fill(Colors.white)
        # stop music while game paused
        self.music.stop()

        # Assign variables
        self.pause = True
        # Loop
        while self.pause:
            # Timer
            self.clock.tick(30)

            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_p:
                        self.pause = False

            # add headline
            self.screen.msg_display('PAUSED',
                                    self.screen.width / 2,
                                    self.screen.height / 4,
                                    100)
            # add continue-Button
            self.screen.button('Continue',
                               300, 270,
                               200, 50,
                               Colors.blue, Colors.bright_blue,
                               Colors.white,
                               self.game_continue)

            # Redisplay
            self.screen.flip()

    # unpause the game and go on
    def game_continue(self):
        self.pause = False
        if not self.muted:
            self.music.play(-1)

    # show main menu
    def show_mainmenu(self):
        # fill background with color white
        self.screen.fill(Colors.white)

        # Assign variables
        button_width = 200
        button_height = 50
        menu_y_start = 200
        menu_y_gap = 20
        menu_isshown = True

        # Loop
        while menu_isshown:
            # Timer
            self.clock.tick(30)

            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    menu_isshown = False
                    self.game_quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.game_quit()

            # fill background with defined background image from constructor
            self.screen.blit(self.background_menu, (0, 0))
            # add headline
            self.screen.msg_display("Hit the mole!",
                                    self.screen.width / 2,
                                    self.screen.height / 5,
                                    100)
            # add new_game-Button
            self.screen.button('New Game',
                               self.screen.width / 2 - button_width / 2,  # x-Pos
                               menu_y_start,  # y-Pos
                               button_width,
                               button_height,
                               Colors.green,  # inactive Color
                               Colors.bright_green,  # active Color
                               Colors.black,  # Text-Color
                               self.game_new  # action when clicked
                               )
            # add show_highscore-Button
            self.screen.button('Highscore',
                               self.screen.width / 2 - button_width / 2,
                               menu_y_start + button_height + menu_y_gap,
                               button_width,
                               button_height,
                               Colors.blue, Colors.bright_blue,
                               Colors.white,
                               self.highscore.display_highscore
                               )
            # add show_options-Button
            self.screen.button('Options',
                               self.screen.width / 2 - button_width / 2,
                               menu_y_start + button_height * 2 + menu_y_gap * 2,
                               button_width,
                               button_height,
                               Colors.orange, Colors.bright_orange,
                               Colors.white,
                               self.show_options
                               )
            # add show_help-Button
            self.screen.button('Help',
                               self.screen.width / 2 - button_width / 2,
                               menu_y_start + button_height * 3 + menu_y_gap * 3,
                               button_width,
                               button_height,
                               Colors.violett, Colors.bright_violett,
                               Colors.white,
                               self.show_help
                               )
            # add quit_game-Button
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

    # start main game loop
    def game_loop(self):
        # initialy fill backgrpund with color white
        self.screen.fill(Colors.white)

        # Assign variables
        # define a sprite group to render all on game world placed objects
        sprite_group = Group()
        sprite_group.add(self.mole)         # add the mole
        sprite_group.add(self.shovel)       # add the shovel

        # initialize game by settings game variables to zero
        self.points = 0
        self.count_fails = 0
        # start endless playing game music
        if not self.muted:
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
                        self.points += self.game_level
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
                    pygame.time.set_timer(USEREVENT, self.escape_timer)
                    self.screen.blit(self.background_game, (0, 0))
                    sprite_group.update(pygame.mouse.get_pos())
                    sprite_group.draw(self.screen.get_screen())
                    self.screen.msg_hud_left(u'Fehler: ' +
                                             str(self.count_fails),
                                             15, self.screen.height - 45,
                                             18, Colors.white)
                    self.screen.msg_hud_left(u'Punkte: ' +
                                             str(self.points),
                                             15, self.screen.height - 15,
                                             18, Colors.white)
                    break
                elif event.type == KEYDOWN:
                    if event.key == K_p:
                        self.pause = True
                        self.game_pause()
                    if event.key == K_m:
                        self.toogle_muted()
                        if self.muted:
                            self.music.stop()
                        else:
                            self.music.play(-1)
                    if event.key == K_ESCAPE:
                        running = False
                        self.music.stop()
                        self.show_mainmenu()

            # Redisplay
            self.screen.flip()

    # start method to start pygame with the main menu
    def start(self):
        self.show_mainmenu()

    # create and start a new game
    def game_new(self):
        self.isfinished = False
        self.pause = False

        self.points = 0
        self.count_fails = 0

        self.game_loop()
