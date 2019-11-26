#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'Oliver Banse'

# IDEA
# Import and Initialization
import pygame
from pygame.locals import *
pygame.init()


#colors
black = (0,0,0)
white = (255,255,255)

# Display configuration
display_width = 800
display_height = 600
size = (display_width, display_height)
screen = pygame.display.set_mode(size)
screen.fill(white)
pygame.display.set_caption('MainMenu')


# Entities
def text_objects(text, font, color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2, display_height/2))
    screen.blit(TextSurf, TextRect)

# Action --> ALTER
def main():
    # Assign variables
    running = True
    clock = pygame.time.Clock()

    message_display("MAINMENU")
    # TODO: hier gehts weiter:
    #  https://www.youtube.com/watch?v=dX57H9qecCU&list=PLQVvvaa0QuDdLkP8MrOXLe_rKuf6r80KO&index=5

    # Loop
    while running:
        # Timer
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            print(event)
        # Redisplay

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
