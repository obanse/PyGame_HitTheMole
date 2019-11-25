#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'Oliver Banse'

# I_mport and Initialize
import pygame
from pygame.locals import *
pygame.init()

# D_isplay configuration
size = (640, 480)
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
pygame.display.set_caption('Paint Brush')

# E_ntities
brush = pygame.image.load('black_brush.png')
brush = pygame.transform.scale(brush, (64, 64))

# A_ction --> ALTER
# A_ssign variables
running = True
paint = False
clock = pygame.time.Clock()
brush_rect = brush.get_rect()
speed = [2, 2]

# L_oop
while running:
    # T_iming
    clock.tick(60)

    # E_vents
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            break

    brush_rect = brush_rect.move(speed)
    if brush_rect.left < 0 or brush_rect.right > size[0]:
        speed[0] = -speed[0]
    if brush_rect.top < 0 or brush_rect.bottom > size[1]:
        speed[1] = -speed[1]

    # R_epaint (R_display)
    screen.fill((255,255,255))
    screen.blit(brush, brush_rect)
    pygame.display.update()
