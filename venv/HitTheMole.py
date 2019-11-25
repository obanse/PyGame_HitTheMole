#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'Oliver Banse'


# TODO:
# - Strafpunkte, max 3
# - Spiel starten, Spiel beenden, Namen eingeben für Highscores
# - Bestenliste, speichern in Datei
# - Zufällige Zeit der Neuerscheingung des Maulwurfs
# - Mauszeiger als Schaufel
# - Überarbeitung des Maulwurfs
# - Dimensionierung, wenn Maulwurf im Hintergrund, dann kleiner als im Vordergrund

# I_mport and Initialize
import pygame
from pygame.locals import *
import random
pygame.init()

# D_isplay configuration
display_width = 1024
display_height = 768
size = (display_width, display_height)

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Hit the mole!')

# E_ntities
class Mole(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # visualization
        #self.image = pygame.image.load('images/mole.png')
        self.image = pygame.image.load('images/mole.gif')
        self.image = pygame.transform.scale(self.image, (60, 96))
        # hitzone
        self.rect = self.image.get_rect()
        # sound when hitted
        self.sound = pygame.mixer.Sound('sounds/mole_ow.wav')
        # position on screen
        self.rect.left = random.randint(0, 964)
        self.rect.top = random.randint(236, 670)

    def flee(self):
        # new position on screen
        self.rect.left = random.randint(0, 964)
        self.rect.top = random.randint(236, 670)

    def cry(self):
        self.sound.play()

    def hitted(self, pos):
        return self.rect.collidepoint(pos)

class Shovel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # visualization
        self.image = pygame.image.load('images/shovel.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

mole = Mole()
shovel = Shovel()

sprite_group = pygame.sprite.Group()
sprite_group.add(mole)
sprite_group.add(shovel)

#bg = pygame.image.load('images/grass_field.jpg')
bg = pygame.image.load('images/landscape.png')
bg = pygame.transform.scale(bg, (size))

bg_red = pygame.Surface(size)
bg_red = bg_red.convert()
bg_red.fill((255,0,0))

font = pygame.font.Font(None, 25)

# A_ction --> ALTER
# A_ssigning variables
running = True
count_hits = 0
clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT, 200)

music = pygame.mixer.Sound('sounds/whack.wav')
music.play(-1)


# L_oop (game-loop)
while running:
    # T_iming
    clock.tick(60)

    # E_vent handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            break
        elif event.type == MOUSEBUTTONDOWN:
            if mole.hitted(pygame.mouse.get_pos()):
                mole.cry()
                count_hits += 1
                screen.blit(bg_red, (0,0))
                break
            else:
                break
        elif event.type == USEREVENT:
            mole.flee()
            pygame.time.set_timer(USEREVENT, 1000)
            screen.blit(bg, (0,0))
            sprite_group.update()
            sprite_group.draw(screen)
            text = font.render(u'Maulfwürfe gefangen: '
                               + str(count_hits), True, Color('white'))
            screen.blit(text, (10, 740))
            break

    # R_epaint
    pygame.display.flip()