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
lines = []
planets = []


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
        self.r = lvl * 7 + 10
        self.highlighting = 0
        self.font = "Times " + str(int(12 * math.sqrt(self.level)))
        self.growing = 0
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
        self.id = canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color,
            outline='grey'
        )
        self.text = canvas.create_text(self.x, self.y, text=int(self.mass), fill='white', font=self.font)

    def first_click(self):
        self.highlighting = 1
        self.id = canvas.create_oval(
            self.x - self.r - 5,
            self.y - self.r - 5,
            self.x + self.r + 5,
            self.y + self.r + 5,
            width=3,
            outline='grey'
        )

    def second_click(self, other):
        if self != other:
            l = Line(self, other)
            lines.append(l)
        else:
            if (self.mass >= self.level * 21) and (self.level < 4):
                self.growing = 7
                self.level += 1

    def grow(self):
        if self.growing > 0:
            self.r += 1
            self.mass -= 3 * (self.level - 1)
            canvas.delete(self.id)
            self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                outline='grey'
            )
            canvas.delete(self.text)
            self.text = canvas.create_text(self.x, self.y, text=int(self.mass), fill='white', font=self.font)
            self.growing -= 1
        else:
            self.font = "Times " + str(int(12 * math.sqrt(self.level)))
            canvas.delete(self.text)
            self.text = canvas.create_text(self.x, self.y, text=int(self.mass), fill='white', font=self.font)

    def massupdate(self):
        if self.mass < 25 * (2 ** self.level):
            self.mass += self.level/10
            canvas.delete(self.text)
            self.text = canvas.create_text(self.x, self.y, text=int(self.mass), fill='white', font=self.font)

    def redraw(self):
        canvas.delete(self.id)
        self.id = canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color,
            outline='grey'
        )


class Line:
    def __init__(self,
                 p1,
                 p2
    ):
        self.color = p1.color
        self.an = math.atan2((p2.y - p1.y), (p2.x - p1.x))
        print(self.an)
        self.x1 = p1.x + p1.r * math.cos(self.an)
        self.y1 = p1.y + p1.r * math.sin(self.an)
        self.x2 = p2.x - p2.r * math.cos(self.an)
        self.y2 = p2.y - p2.r * math.sin(self.an)
        self.line_coords = [self.x1, self.y1, self.x2, self.y2]
        self.begin = 1
        self.end = 0
        self.planet1 = p1
        self.planet2 = p2
        self.Num = p1.mass
        self.max = 0
        self.count1 = 0
        self.count2 = 0
        self.velocity = 10
        self.r = ((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2) ** 0.5
        self.max = int(self.r / self.velocity)

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

    def grow(self):
        if self.count1 < self.max:
            self.count1 += 1
        elif (self.count1 >= self.max) and (self.count1 < self.Num):
            self.count1 += 1
            self.end = 1
        elif self.count2 < self.max:
            self.count2 += 1
            self.begin = 0
        else:
            self.stop()
            self.end = 0
        self.update_mass()

    def redraw(self):
        canvas.coords(
            self.id,
            *self.get_line_begin(),
            *self.get_line_end(),
        )

    def update_mass(self):
        if self.begin == 1 and self.end == 1:
            self.planet1.mass -= 1
            if self.planet2.owner == self.planet1.owner:
                self.planet2.mass += 1
            else:
                self.planet2.mass -= 1
                if self.planet2.mass < 0:
                    self.capture()
        elif self.begin == 1:
            self.planet1.mass -= 1
        elif self.end == 1:
            if self.planet2.owner == self.planet1.owner:
                self.planet2.mass += 1
            else:
                self.planet2.mass -= 1
                if self.planet2.mass < 0:
                    self.capture()

    def capture(self):
        self.planet2.color = self.planet1.color
        self.planet2.owner = self.planet1.owner
        self.planet2.lvl = 1
        self.planet2.redraw()

    def stop(self):
        canvas.delete(self.id)


def click(event):
    sec_click = 0
    i = 0
    for i in planets:
        if i.highlighting == 1:
            sec_click = 1
            break

    if sec_click == 1:
        for j in planets:
            if ((event.x - j.x) ** 2 + (event.y - j.y) ** 2) <= (j.r) ** 2:
                i.second_click(j)
                break
        i.highlighting = 0
        canvas.delete(i.id)
    else:
        for j in planets:
            if ((event.x - j.x) ** 2 + (event.y - j.y) ** 2) <= (j.r) ** 2:
                j.first_click()


def update():
    for i in lines:
        i.grow()
        i.redraw()
    for j in planets:
        j.grow()
        j.massupdate()
    root.after(100, update)


def main():
    global planets
    p1 = Planet(20, 400, 400, 1, 2)
    p2 = Planet(20, 500, 500, 0, 2)
    p3 = Planet(20, 600, 200, 2, 2)
    planets = [p1, p2, p3]
    canvas.bind('<Button-1>', click)
    update()


main()

root.mainloop()
