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
        elif self.owner == 2:
            self.color = 'red'
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
            l = UnitsLine(self.x, self.y, other.x, other.y, self.color, self.mass)
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


class UnitsLine:
    def __init__(self,
                 x1,
                 y1,
                 x2,
                 y2,
                 color,
                 ):
        pass
        '''self.r = 5
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
        )'''


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
        i.linemove()
    for i in planets:
        i.grow()
        i.massupdate()
    root.after(100, update)


def main():
    global planets
    p1 = Planet(20, 400, 400, 0, 1)
    p2 = Planet(30, 500, 500, 1, 2)
    planets = [p1, p2]
    canvas.bind('<Button-1>', click)
    update()


main()
root.mainloop()