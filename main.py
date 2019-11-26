from random import randrange as rnd, choice
import tkinter as tk
import math
import time
import socket
import pickle

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('1920x1080')
canv = tk.Canvas(root, bg='black')
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
        self.font = "Times " + str(12 * self.lvl)
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
            fill=self.color,
            outline='grey'
        )
        canv.create_text(self.x, self.y, text=self.mass, fill='white', font=self.font)

    def first_click(self):
        self.highliting = 1
        self.id = canv.create_oval(
            self.x - self.radc * self.lvl - 5,
            self.y - self.radc * self.lvl - 5,
            self.x + self.radc * self.lvl + 5,
            self.y + self.radc * self.lvl + 5,
            width=3,
            outline='grey'
        )
        print('first_click')

    def second_click(self, other):
        print('second_click')


def click(event):
    sec_click = 0
    i = 0
    for i in planets:
        if i.highliting == 1:
            sec_click = 1
            break
    print(i.lvl)
    if sec_click == 1:
        for j in planets:
            if ((event.x - j.x) ** 2 + (event.y - j.y) ** 2) <= (j.radc * j.lvl) ** 2:
                i.second_click(j)
                break
        i.highliting = 0
        canv.delete(i.id)
    else:
        for j in planets:
            if ((event.x - j.x) ** 2 + (event.y - j.y) ** 2) <= (j.radc * j.lvl) ** 2:
                j.first_click()


p1 = Planet(20, 400, 400, 1, 1)
p2 = Planet(20, 500, 500, 1, 2)
planets = [p1, p2]
canv.bind('<Button-1>', click)
root.mainloop()
