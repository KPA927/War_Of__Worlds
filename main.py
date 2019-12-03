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
        self.mass_limit = 0
        self.mass_grow = 0
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
            self.mass_limit = self.level * 100
            self.mass_grow = self.level * 5
        elif self.owner == 2:
            self.color = 'red'
            self.mass_limit = self.level * 100
            self.mass_grow = self.level * 5
        else:
            self.color = 'grey'
            self.mass_limit = self.level * 50
            self.mass_grow = self.level * 2
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
        pass

    def grow(self):
        if self.mass < self.mass_limit:
            self.mass += self.mass_grow
            if self.mass > self.mass_limit:
                self.mass = self.mass_limit
        time.sleep(1)
        root.after(1, self.grow)

class Line:
    def __init__(self,
                 p1,
                 p2
    ):
        self.color = p1.clr

        self.an = math.atan2((p2.x - p1.x), (p2.y - p1.y))
        self.x1 = p1.x + p1.r * math.cos(self.an)
        self.y1 = p1.y - p1.r * math.sin(self.an)
        self.x2 = p2.x - p2.r * math.cos(self.an)
        self.y2 = p2.y + p2.r * math.sin(self.an)
        self.line_coords = [self.x1, self.y1, self.x2, self.y2]
        self.begin = 1
        self.end = 0
        self.Num = p1.mass
        self.max = 0
        self.count1 = 0
        self.count2 = self.max
        self.velocity = 10
        self.max = int(self.r / self.velocity)
        self.r = ((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2) ** 0.5

        self.id = canvas.create_line(self.get_line_begin(),
                                     self.get_line_end(),
                                     fill=self.color,
                                     width=7
                                     )

    def get_line_begin(self):
        if self.begin == 1:
            x = self.line_coords[0]
            y = self.line_coords[1]
        else:
            length = self.count2 * self.velocity
            x = (self.line_coords[0] + length * math.cos(self.an))
            y = (self.line_coords[1] + length * math.sin(self.an))
        return x, y

    def get_line_end(self):
        if self.count1 <= self.max:
            length = self.count1 * self.velocity
        else:
            length = self.r
        x = (self.line_coords[0] + length * math.cos(self.an))
        y = (self.line_coords[1] + length * math.sin(self.an))

        return x, y

    def grow(self, planet_1, other):
        if self.count1 < self.max:
            self.count1 += 1
            self.update_mass(planet_1, other)
        elif (self.count1 >= self.max) and (self.count1 < self.Num):
            self.count1 += 1
            self.end = 1
            self.update_mass(planet_1, other)
        else:
            self.count2 += 1
            self.begin = 0
            self.update_mass(planet_1, other)

    def redraw(self):
        canvas.coords(
            self.id,
            *self.get_line_begin(),
            *self.get_line_end(),
        )

    def update_mass(self, planet_1, planet_2):
        if self.begin == 1 and self.end == 1:
            planet_1.mass -= 1
            planet_2.mass += 1
        elif self.begin == 1:
            planet_1.mass -= 1
        elif self.end == 1:
            planet_2.mass += 1


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


#def main():
 #   for i in planets:
  #      i.grow()

p1 = Planet(20, 400, 400, 0, 1)
p2 = Planet(20, 500, 500, 1, 2)
planets = [p1, p2]
canvas.bind('<Button-1>', click)
#main()
root.mainloop()
