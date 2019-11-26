from random import randrange as rnd, choice
import tkinter as tk
import math
import time
import socket
import pickle


root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.focus_set()
canv.pack(fill=tk.BOTH, expand=1)


class Planet:
    def __init__(self, m, x, y, ow, l):
        self.mass = m
        self.x = x
        self.y = y
        self.lvl = l
        self.owner = ow
        self.radc = 15
        self.highliting = 0
        if self.owner == 1:
            self.color = 'blue'
        elif self.owner == 2:
            self.color = 'red'
        else:
            self.color = 'grey'
        canv.create_oval(
            self.x - self.radc * self.lvl,
            self.y - self.radc * self.lvl,
            self.x + self.radc * self.lvl,
            self.y + self.radc * self.lvl,
            fill=self.color
        )

    def first_click(self, event):
        if ((event.x - self.x)**2 + (event.y - self.y)**2) <= (self.radc * self.lvl)**2:
            self.highliting = 1
            canv.create_oval(
                self.x - self.radc * self.lvl - 5,
                self.y - self.radc * self.lvl - 5,
                self.x + self.radc * self.lvl + 5,
                self.y + self.radc * self.lvl + 5,
                weight = 3)


p1 = Planet(1, 400, 400, 1, 1)
root.mainloop()