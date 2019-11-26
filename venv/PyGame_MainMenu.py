#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'Oliver Banse'


# TODO:
# - Highscores -> zurück Button
# - Namen eingeben für Highscores
# - Optionen ausdenken, (Bsp.: Musik abschalten, Sounds abschalten, ...)
# - Hilfe-Seite mit zurück-Button und Tasten (Bsp.: F1 - Help, P_ause, M_uted, Esc_ape
# - Zufällige Zeit des Neuerscheinen des Maulwurfs
# - Überarbeitung des Maulwurfs
# - Dimensionierung, wenn Maulwurf im Hintergrund, dann kleiner als im Vordergrund

# IDEA
# Import and Initialization
import json
import random
import time
from operator import itemgetter

import pygame
from pygame.locals import *
from pygame.sprite import Group
from pygame.sprite import Sprite

pygame.init()

# Display configuration
screen_width = 800
screen_height = 600
size = (screen_width, screen_height)
clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT, 200)

# game settings
screen = pygame.display.set_mode(size)
pygame.display.set_caption('MainMenu')
music = pygame.mixer.Sound('sounds/whack.wav')
pause = False
muted = False

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


# Entities
class Mole(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # visualization
        self.width = 60
        self.height = 96
        self.image = pygame.image.load('images/mole.gif')
        self.image = pygame.transform.scale(self.image,
                                    (self.width, self.height))
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound('sounds/mole_ow.wav')
        self.__place()

    def __place(self):
        self.rect.left = random.randint(0, screen_width-self.width)
        self.rect.top = random.randint(230, screen_height-self.height)

    def escape(self):
        self.__place()

    def cry(self):
        self.sound.play()

    def hitted(self, pos):
        return self.rect.collidepoint(pos)


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
        self.update()

    def update(self):
        self.rect.left, self.rect.top = pygame.mouse.get_pos()


def load_highscore():
    try:
        with open('highscores.json', 'r') as file:
            highscores = json.load(file)
    except FileNotFoundError:
        return []

    return sorted(highscores, key=itemgetter(1), reverse=True)
#highscores = load_highscore()


def save_highscores(highscores):
    with open('highscores.json', 'w') as file:
        json.dump(highscores, file)


def do_highscore():
    # wenn highscores[len(highscores)][1] < count_hits ->
    #   --> highscores.pop(), highscores.append([%NAME%, count_hits])
    #   --> save_highscores
    #print(highscores)
    if len(highscores[0]) <= 9:
        highscores.append(["Ingo", 17])


def add_highscore(count_hits):
    highscores = load_highscore()

    if len(highscores[0]) < 9:
        # TODO: create window to input text!
        name = get_name()
        highscores.append([name, count_hits])
    elif highscores[len(highscores)][1] < count_hits:
        # TODO: create window to input text!
        name = get_name()
        highscores.pop(len(highscores[0]))
        highscores.append([name, count_hits])
    save_highscores(highscores)


def display_highscore():
    font = pygame.font.Font('freesansbold.ttf', 20)
    highscores = load_highscore()

    while True:
        screen.fill(white)
        # Display the high-scores.
        msg_display('Highscore', screen_width/2, screen_height/5, 100)

        for y, (hi_name, hi_score) in enumerate(highscores):
            TextSurf, TextRect = text_objects(f'{hi_name} {hi_score}', font, blue)
            TextRect.left, TextRect.top = ((350, y * 30 + 200))
            screen.blit(TextSurf, TextRect)

        for event in pygame.event.get():
            if event.type == QUIT:
                game_quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_menu()
                if event.key == K_a:
                    # TODO: create logic to test --> add_highscore()
                    print("Add a person")

        button('Go Back', screen_width / 2 - 90, 520, 180, 40,
               blue, bright_blue, white, game_menu)

        pygame.display.flip()
        clock.tick(30)



def text_objects(text, font, color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(text, x, y, width, height, inactive_color, active_color,
           text_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+width > mouse[0] > x and y+height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] and action != None:
            action()
        elif click[0] and action == None:
            print(text + '-Button clicked!')
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    font = pygame.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = text_objects(text, font, text_color)
    textRect.center = ((x+(width/2)),(y+(height/2)))
    screen.blit(textSurf, textRect)


def msg_display(text, x, y, font_size=32, font_color=black):
    font = pygame.font.Font('freesansbold.ttf', font_size)
    TextSurf, TextRect = text_objects(text, font, font_color)
    TextRect.center = ((x, y))
    screen.blit(TextSurf, TextRect)


def msg_hud_left(text, x, y, font_size=12, font_color=black):
    font = pygame.font.Font('freesansbold.ttf', font_size)
    TextSurf, TextRect = text_objects(text, font, font_color)
    TextRect.left, TextRect.bottom = ((x, y))
    screen.blit(TextSurf, TextRect)


def msg_hud_right(text, x, y, font_size=12, font_color=black):
    font = pygame.font.Font('freesansbold.ttf', font_size)
    TextSurf, TextRect = text_objects(text, font, font_color)
    TextRect.right, TextRect.bottom = ((x, y))
    screen.blit(TextSurf, TextRect)

def game_quit():
    pygame.quit()
    quit()

# Action --> ALTER
def game_over(count_hits):
    screen.fill(white)
    music.fadeout(2000)
    msg_display('GAME OVER', screen_width/2, screen_height/4, 100)
    msg_display(u'Maulfwürfe gefangen: ' + str(count_hits),
                    screen_width / 2, screen_height / 2, 40, blue)
    pygame.display.flip()
    time.sleep(3)
    game_menu()


def game_continue():
    global pause
    pause = False
    music.play(-1)


def game_pause():
    screen.fill(white)
    music.stop()

    # Assign variables
    global pause

    # Loop
    while pause:
        # Timer
        clock.tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        msg_display('PAUSED', screen_width / 2, screen_height / 4, 100)
        button('Continue', 300, 270, 200, 50, blue, bright_blue, white,
            game_continue)

        # Redisplay
        pygame.display.flip()


# Action --> ALTER
def game_menu():
    screen.fill(white)

    bg = pygame.image.load('images/grass_field.jpg')
    bg = pygame.transform.scale(bg, (size))

    # Assign variables
    button_width = 200
    button_height = 50
    menu_y_start = 200
    menu_y_gap = 20

    # Loop
    intro = True
    while intro:
        # Timer
        clock.tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        # screen.fill(white)
        screen.blit(bg, (0,0))

        msg_display("Hit the mole!", screen_width/2, screen_height/5, 100)

        button_width = 200
        button_height = 50
        menu_y_start = 200
        menu_y_gap = 20

        button('New Game',
               screen_width / 2-button_width / 2,   # x-Position
               menu_y_start,                        # y-Position
               button_width,
               button_height,
               green, bright_green,                 # inactive-, active-,
               black,                               # and text-color
               game_loop                            # action when clicked
               )
        button('Highscore',
               screen_width / 2 - button_width / 2,
               menu_y_start + button_height + menu_y_gap,
               button_width,
               button_height,
               blue, bright_blue,
               white,
               display_highscore
               )
        button('Options',
               screen_width/2-button_width/2,
               menu_y_start + button_height * 2 + menu_y_gap * 2,
               button_width,
               button_height,
               orange, bright_orange,
               white
               )
        button('Help',
               screen_width/2-button_width/2,
               menu_y_start + button_height * 3 + menu_y_gap * 3,
               button_width,
               button_height,
               violett, bright_violett,
               white
               )
        button('Quit Game',
               screen_width/2-button_width/2,
               menu_y_start + button_height * 4 + menu_y_gap * 4,
               button_width,
               button_height,
               red, bright_red,
               white,
               game_quit
               )

        # Redisplay
        pygame.display.flip()


# Action --> ALTER
def game_loop():
    global pause, count_hits, count_fails, muted

    screen.fill(white)

    # Assign variables
    mole = Mole()
    shovel = Shovel()

    sprite_group = Group()
    sprite_group.add(mole)
    sprite_group.add(shovel)

    bg = pygame.image.load('images/landscape.png')
    bg = pygame.transform.scale(bg, (size))

    bg_red = pygame.Surface(size)
    bg_red = bg_red.convert()
    bg_red.fill(red)
    font = pygame.font.Font(None, 25)

    count_hits = 0
    count_fails = 0
    music.play(-1)

    # Loop
    running = True
    while running:
        # Timing
        clock.tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                game_quit()
                break
            elif event.type == MOUSEBUTTONDOWN:
                if mole.hitted(pygame.mouse.get_pos()):
                    mole.cry()
                    count_hits += 1
                    screen.blit(bg_red, (0,0))
                    break
                else:
                    if count_fails < 3:
                        count_fails += 1
                    else:
                        game_over(count_hits)
                    pygame.mixer.Sound('sounds/error.wav').play()
                    break
            elif event.type == USEREVENT:
                mole.escape()
                pygame.time.set_timer(USEREVENT, 1000)
                screen.blit(bg, (0,0))
                sprite_group.update()
                sprite_group.draw(screen)
                msg_hud_left(u'Fehler: ' + str(count_fails),
                             15, screen_height - 45, 18, white)
                msg_hud_left(u'Maulfwürfe gefangen: ' + str(count_hits),
                             15, screen_height - 15, 18, white)
                break
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    pause = True
                    game_pause()
                if event.key == K_m:
                    muted = not muted
                    if muted:
                        music.stop()
                    else:
                        music.play(-1)

        # Redisplay
        pygame.display.flip()


if __name__ == '__main__':
    game_menu()
