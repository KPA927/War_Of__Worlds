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

counter = 0


def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb


class Planet:
    def __init__(self,
                 mass,
                 x,
                 y,
                 owner,
                 lvl):
        self.mass = mass
        self.mass_limit = 0
        self.x = x
        self.y = y
        self.id1 = 0
        self.level = lvl
        self.owner = owner
        self.r = lvl * 7 + 10
        self.highlighting = 0
        self.font = "Times " + str(int(12 * math.sqrt(self.level)))
        self.growing = 0
        if self.mass <= 235:
            if self.owner == 1:
                self.color = _from_rgb((52, 235 - int(self.mass), 235))
            elif self.owner == 2:
                self.color = _from_rgb((235, 235 - int(self.mass), 52))
            else:
                self.color = _from_rgb((128, 128, 128))
        else:
            if self.owner == 1:
                self.color = _from_rgb((52, 0, 235))
            elif self.owner == 2:
                self.color = _from_rgb((235, 0, 52))
            else:
                self.color = _from_rgb((128, 128, 128))
        if self.owner == 1:

            self.mass_limit =  25 * (2 ** self.level)
        elif self.owner == 2:
            self.mass_limit =  25 * (2 ** self.level)
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
        self.id1 = canvas.create_oval(
            self.x - self.r - 5,
            self.y - self.r - 5,
            self.x + self.r + 5,
            self.y + self.r + 5,
            width=3,
            outline='grey'
        )

    def second_click(self, other):
        if self != other:
            start = self.owner
            end = other.owner
            mass = self.mass
            color = self.color
            print(start, end)
            l = Line(self, other, start, end, mass, color)
            lines.append(l)
        else:
            if (self.mass >= self.level * 21) and (self.level < 4):
                self.growing = 7
                self.level += 1

    def grow(self):
        if self.growing > 0:
            self.r += 0.1
            self.mass -= 0.3 * (self.level - 1)
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
            self.growing -= 0.1
        else:
            self.font = "Times " + str(int(12 * math.sqrt(self.level)))
            canvas.delete(self.text)
            self.text = canvas.create_text(self.x, self.y, text=int(self.mass), fill='white', font=self.font)

    def massupdate(self):
        if self.mass < 25 * (2 ** self.level):
            self.mass += self.level/100
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
        self.text = canvas.create_text(self.x, self.y, text=int(self.mass), fill='white', font=self.font)

    def colorupdate(self):
        if self.mass <= 235:
            if self.owner == 1:
                self.color = _from_rgb((52, 235 - int(self.mass), 235))
            elif self.owner == 2:
                self.color = _from_rgb((235, 235 - int(self.mass), 52))
            else:
                self.color = _from_rgb((128, 128, 128))
        else:
            if self.owner == 1:
                self.color = _from_rgb((52, 0, 235))
            elif self.owner == 2:
                self.color = _from_rgb((235, 0, 52))
            else:
                self.color = _from_rgb((128, 128, 128))
        self.redraw()


class Line:
    def __init__(self,
                 p1,
                 p2,
                 start,
                 end,
                 mass,
                 color
    ):
        self.color = p1.color
        self.an = math.atan2((p2.y - p1.y), (p2.x - p1.x))
        self.x1 = p1.x + p1.r * math.cos(self.an)
        self.y1 = p1.y + p1.r * math.sin(self.an)
        self.x2 = p2.x - p2.r * math.cos(self.an)
        self.y2 = p2.y - p2.r * math.sin(self.an)
        self.line_coords = [self.x1, self.y1, self.x2, self.y2]
        self.begin = 1
        self.end = 0
        self.planet1 = p1
        self.planet2 = p2
        self.color =color
        self.o_start = start
        self.o_end = end
        self.Num = mass
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
        if self.Num <= self.max:
            if self.count1 < self.Num:
                self.count1 += 0.1
            elif (self.count1 >= self.Num) and (self.count1 < self.max):
                self.begin = 0
                self.count1 += 0.1
                self.count2 += 0.1
            elif (self.count1 >= self.max) and (self.count2 <= self.max):
                self.end = 1
                self.count2 += 0.1
            else:
                self.stop()

        if self.Num > self.max:
            if self.count1 < self.max:
                self.count1 += 0.1
            elif self.count1 < self.Num:
                self.count1 += 0.1
                self.end = 1
            elif self.count2 < self.max:
                self.count2 += 0.1
                self.begin = 0
            else:
                self.stop()

        self.update_mass()

    def redraw(self):
        canvas.coords(
            self.id,
            *self.get_line_begin(),
            *self.get_line_end(),
        )

    def update_mass(self):
        if self.begin == 1 and self.end == 1:
            self.planet1.mass -= 0.1
            if self.o_start == self.o_end:
                self.planet2.mass += 0.1
            else:
                self.planet2.mass -= 0.1
                if self.planet2.mass <= 0:
                    self.capture()
        elif self.begin == 1:
            self.planet1.mass -= 0.1
        elif self.end == 1:
            if self.o_start == self.o_end:
                self.planet2.mass += 0.1
            else:
                self.planet2.mass -= 0.1
                if self.planet2.mass <= 0:
                    self.capture()

    def capture(self):
        self.planet2.color = self.color
        self.planet2.owner = self.o_start
        self.o_end = self.o_start
        self.planet2.redraw()

    def stop(self):
        canvas.delete(self.id)
        self.begin = 0
        self.end = 0
        lines.remove(self)


def click(event):
    sec_click = 0
    i = 0
    allow = 1
    for i in planets:
        if i.highlighting == 1:
            sec_click = 1
            break

    if sec_click == 1:
        for j in planets:
            if ((event.x - j.x) ** 2 + (event.y - j.y) ** 2) <= (j.r) ** 2:
                for k in lines:
                    if k.planet1 == i and k.planet2 == j:
                        allow = 0
                if i.mass <= 0:
                    allow = 0
                if allow == 1:
                    i.second_click(j)
                    break
                allow = 1
        i.highlighting = 0
        canvas.delete(i.id1)
    else:
        for j in planets:
            if (((event.x - j.x) ** 2 + (event.y - j.y) ** 2) <= (j.r) ** 2) and (j.owner == 1):
                j.first_click()


def II():
    global planets
    my_planets = []
    other_planets = []
    allow = 1
    target = 0
    length = 5000
    exit = 0
    attak_potensial = 0
    for i in planets:
        if i.owner == 2:
            if i.mass == 25 * (2 ** i.level):
                i.second_click(i)
            else:
                my_planets.append(i)
        else:
            other_planets.append(i)
    if len(my_planets) != 0 and len(other_planets) != 0:
        for i in my_planets:
            attak_potensial += i.mass
        while exit <= len(other_planets):
            for i in my_planets:
                for j in other_planets:
                    if (i.x - j.x) ** 2 + (i.y - j.y) ** 2 <= length ** 2:
                        length = ((i.x - j.x) ** 2 + (i.y - j.y) ** 2) ** 0.5
                        target1 = j
            if target1.mass < attak_potensial:
                target = target1
                break
            else:
                other_planets.remove(target1)
                exit += 1
            length = 5000
        if target != 0:
            for i in my_planets:
                for k in lines:
                    if k.planet1 == i and k.planet2 == target:
                        allow = 0
                if i.mass <= 0:
                    allow = 0
                if allow == 1:
                    i.second_click(target)
                allow = 1


def update():
    global counter
    if counter >= 500:
        counter = 0
        II()
    for i in lines:
        i.grow()
        i.redraw()
    for j in planets:
        j.grow()
        j.massupdate()
        if counter % 50 == 0:
            j.colorupdate()
    counter += 1
    root.after(10, update)


def main():
    global planets
    p1 = Planet(20, 400, 400, 1, 2)
    p2 = Planet(100, 500, 500, 1, 2)
    p3 = Planet(200, 400, 300, 1, 1)
    planets = [p1, p2, p3]
    canvas.bind('<Button-1>', click)
    update()


main()

root.mainloop()
