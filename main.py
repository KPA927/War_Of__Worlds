from random import randrange as rnd, choice
import tkinter as tk
import math
import time
import socket
import pickle

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('1920x1080')
canvas = tk.Canvas(root, bg='black')
canvas.focus_set()
canvas.pack(fill=tk.BOTH, expand=1)


class Planet:
    def __init__(self,
                 mass,
                 x,
                 y,
                 owner,
                 lvl):
        self.mass = mass
        self.x = x
        self.y = y
        self.level = lvl
        self.owner = owner
        self.radc = 15
        self.r = self.level * self.radc
        self.highlighting = 0
        self.font = "Times " + str(12 * self.level)
        if self.owner == 1:
            self.color = 'blue'
        elif self.owner == 2:
            self.color = 'red'
        else:
            self.color = 'grey'
        canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color,
            outline='grey'
        )
        self.text = canvas.create_text(self.x, self.y, text=self.mass, fill='white', font=self.font)

    def first_click(self):
        self.highlighting = 1
        self.id = canvas.create_oval(
            self.x - self.radc * self.level - 5,
            self.y - self.radc * self.level - 5,
            self.x + self.radc * self.level + 5,
            self.y + self.radc * self.level + 5,
            width=3,
            outline='grey'
        )
        print('first_click')

    def second_click(self, other):
        self.move(other)

    def move(self, other):
        delta_x = self.x - other.x
        delta_y = -(self.y - other.y)
        angle = math.atan2(delta_x, delta_y)
        mass = self.mass
        for i in range(mass):
            self.mass -= 1
            canvas.itemconfig(self.text, text = self.mass)
            unit = Unit(self.x + self.r * math.cos(angle),
                        self.y -self.r * math.sin(angle),
                        self.color,
                        angle,
                        )
            unit.move(other)

    def grow(self):
        pass


class Unit:
    def __init__(self,
                 x,
                 y,
                 clr,
                 angle,
                 ):
        self.r = 5
        self.x = x + self.r * math.cos(angle)
        self.y = y
        print(self.x, x)
        self.color = clr
        self.angle = angle
        self.velocity = 5

        self.time = 2*self.r/self.velocity
        self.id = canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color,
        )

    def move(self, other):
            self.x += self.velocity * math.cos(self.angle)
            self.y -= self.velocity * math.sin(self.angle)
            dr = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
            print(dr)
            if dr <= other.r:
                canvas.delete(self.id)
                canvas.update()
                other.mass += 1
                print('End')
                canvas.itemconfig(other.text, text=other.mass)
            else:
                self.set_coords()
                canvas.update()
                time.sleep(0.1)
                root.after(1, self.move(other))

    def set_coords(self):
        canvas.delete(self.id)
        self.id = canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color,
        )

def click(event):
    sec_click = 0
    i = 0
    for i in planets:
        if i.highlighting == 1:
            sec_click = 1
            break
    print(i.level)
    if sec_click == 1:
        for j in planets:
            if ((event.x - j.x) ** 2 + (event.y - j.y) ** 2) <= (j.radc * j.level) ** 2:
                i.second_click(j)
                break
        i.highlighting = 0
        canvas.delete(i.id)
    else:
        for j in planets:
            if ((event.x - j.x) ** 2 + (event.y - j.y) ** 2) <= (j.radc * j.level) ** 2:
                j.first_click()


p1 = Planet(20, 400, 400, 0, 1)
p2 = Planet(20, 500, 500, 1, 2)
planets = [p1, p2]
canvas.bind('<Button-1>', click)
root.mainloop()
