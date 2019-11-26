#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'Oliver Banse'

# I_mport and initialize
from tkinter import *
import random
import time

# D_isplay configuration


# E_ntities
class Game:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_text(self, canvas, x, y, text, size='40'):
        font = ('Helvetica', size)
        return self.canvas.create_text(x, y, text=text, font=font)

class Ball:
    def __init__(self, canvas, bat, color):
        self.canvas = canvas
        self.bat = bat
        self.id = canvas.create_oval(30, 30, 50, 50, fill=color)
        self.canvas.move(self.id, 100, 200)

        starting_position = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starting_position)
        self.x = starting_position[0]
        self.y = -3

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_bat(self, pos):
        bat_pos = self.canvas.coords(self.bat.id)
        if pos[2] >= bat_pos[0] and pos[0] <= bat_pos[2]:
            if bat_pos[1] <= pos[3] <= bat_pos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)

        if pos[1] <= 0:
            self.y = 6
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True

        if self.hit_bat(pos):
            self.x = -6
        if pos[0] <= 0:
            self.x = 6
        if pos[2] >= self.canvas_width:
            self.x = -6


class Pongbat():
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0

        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<Return>',self.left_turn)
        self.canvas.bind_all('<Return>',self.right_turn)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)

        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= self.canvas_width:
            self.x = 0

    def left_turn(self, evt):
        self.x = -10

    def right_turn(self, evt):
        self.x = 10


# A_ction --> ALTER
# A_ssign
running = True


def main():
    tk = Tk()
    tk.title('Tkinter - Pong PyGame')
    tk.resizable(0, 0)
    tk.wm_attributes('-topmost', 1)
    canvas = Canvas(tk, bg='white', width=640, height=480, bd=0, highlightthickness=0)
    canvas.pack()
    tk.update()

    bat1 = Pongbat(canvas, 'red')
    ball1 = Ball(canvas, bat1, 'green')

    # L_oop
    while running:
        # T_iming
        # E_vent Handling
        # R_epaint
        if not ball1.hit_bottom:
            ball1.draw()
            bat1.draw()
            tk.update()
        else:
            draw1 = Game(canvas)
            draw1.draw_text(canvas, 250, 200, 'Game Over')
            tk.update()
            canvas.after(3000)
            return

        #time.sleep(0.02)
        canvas.after(2)


if __name__ == '__main__':
    main()
