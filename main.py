from random import randrange as rnd, choice
import tkinter as tk
import math
import time
import Gravitation as grav
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
        self.id = canv.create_oval(
            self.x - self.radc * self.lvl,
            self.y - self.radc * self.lvl,
            self.x + self.radc * self.lvl,
            self.y + self.radc * self.lvl,
            fill=self.color
        )

    def first_click(self, event):
        if ((event.x - self.x)**2 + (event.y - self.y)**2) <= (self.radc * self.lvl)**2:
            self.highliting = 1
