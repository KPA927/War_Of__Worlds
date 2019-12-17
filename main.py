# coding=utf-8
from tkinter import *
from random import randrange as rnd, choice
import tkinter as tk
import math
from PIL import Image, ImageTk
#from input_map import read_space_objects_data_from_file as read
import time
import socket
import pickle


root = tk.Tk()
fr = tk.Frame(root)
root.geometry('1920x1080')
lines = []
planets = []
counter = 0
aggressiveness = 0
flag_win = [0, 0]
flag_lose = 0


def casual_game():
    first = Toplevel()
    first.geometry('400x400')
    first['bg'] = 'grey'
    header = Label(first, text="Выберите курс", padx=15, pady=10)
    header.grid(row=0, column=0, sticky=W)

    lang = IntVar()

    python_checkbutton = Radiobutton(first, text="Python", value=1, variable=lang, padx=15, pady=10)
    python_checkbutton.grid(row=1, column=0, sticky=W)

    javascript_checkbutton = Radiobutton(first, text="JavaScript", value=2, variable=lang, padx=15, pady=10)
    javascript_checkbutton.grid(row=2, column=0, sticky=W)

    btn_game = Button(first, text="ОК", background="grey", foreground="white", activebackground="red",
                      activeforeground="green",
                      padx="20", pady="8", font="16", command=lets_play)
    btn_game.place(relx=.5, rely=.2, anchor="c", height=60, width=130, bordermode=OUTSIDE)
    main('7')



def first_game():
    first = Toplevel()
    first.geometry('400x400')
    first['bg'] = 'grey'

    Label(first, text="Правила игры\\"
                      "").pack(expand=1)
    btn_game = Button(first, text="ОК", background="grey", foreground="white", activebackground="red",
                      activeforeground="green",
                      padx="20", pady="8", font="16", command=lets_play)
    btn_game.place(relx=.5, rely=.2, anchor="c", height=60, width=130, bordermode=OUTSIDE)
    main('How_to_play')


def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb



def lets_play():
    root = Tk()
    root.title("Война миров")
    root.geometry("900x900")

    btn1 = Button(text="Начать игру", background="grey", foreground="white", activebackground="red",
                  activeforeground="green",
                  padx="20", pady="8", font="16", command=casual_game)
    btn1.place(relx=.5, rely=.2, anchor="c", height=60, width=130, bordermode=OUTSIDE)

    btn2 = Button(text="Наш проект", background="grey", foreground="white", activebackground="red",
                  activeforeground="green",
                  padx="20", pady="8", font="16", command=first_game)
    btn2.place(relx=.5, rely=.8, anchor="c", height=60, width=130, bordermode=OUTSIDE)

    def animate(frame_number):
        if frame_number > last_frame:
            frame_number = 0
        label.config(image=framelist[frame_number]) 
        root.after(50, animate, frame_number+1)

    label = tk.Label(root, bg='#202020')
    label.pack()

    animate(0)  # Start animation'''


class Planet:
    """Класс планет. Отрисовывает планеты, настраивает взаимодействие между ними.
    Также планеты можно улучшать.

    args **mass** - масса планеты
    **x**, **y** - координаты (x, y) планеты
    **owner** - владелец планеты (1 - игрок, 2 и 3 -боты, 0 - нейтральные планеты)
    **lvl** - уровень планеты (от 1 до 4)
    """
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
        self.busyness = 0
        self.highlighting = 0
        self.font = "Times " + str(int(12 * math.sqrt(self.level)))
        self.growing = 0
        if self.owner == 1:
            self.color = _from_rgb((52, 235 - int(self.level - 1) * 78, 235))
        elif self.owner == 2:
            self.color = _from_rgb((235, 235 - int(self.level - 1) * 78, 52))
        elif self.owner == 3:
            self.color = _from_rgb((52, 235 - int(self.level - 1) * 78, 52))
        else:
            self.color = _from_rgb((128, 128, 128))
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
            self.busyness = 1
            start = self.owner
            end = other.owner
            mass = self.mass
            color = self.color
            owner = self.owner
            l = Line(self, other, start, mass, color, owner)
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
                owner = self.owner
                l = Line(self, other, start, mass, color, owner)
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
            elif 0 >= self.growing:
                self.font = "Times " + str(int(12 * math.sqrt(self.level)))
                if self.owner == 1:
                    self.color = _from_rgb((52, 235 - int(self.level - 1) * 78, 235))
                elif self.owner == 2:
                    self.color = _from_rgb((235, 235 - int(self.level - 1) * 78, 52))
                elif self.owner == 3:
                    self.color = _from_rgb((52, 235 - int(self.level - 1) * 78, 52))
                else:
                    self.color = _from_rgb((128, 128, 128))
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
            

    class Line:
        """Этот класс овечает за отрисовку линий,
        с помощью которых атакуют планеты и пресчет масс"""
        def __init__(self,
                     p1,
                     p2,
                     start,
                     mass,
                     color,
                     owner
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
            self.color = color
            self.o_start = start
            self.Num = mass
            self.owner = owner
            self.max = 0
            self.count1 = 0
            self.count2 = 0
            self.velocity = 30
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
                    self.finish()

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
                    self.finish()
            self.update_mass()

        def redraw(self):
            canvas.coords(
                self.id,
                *self.get_line_begin(),
                *self.get_line_end()
            )

        def update_mass(self):
            if self.begin == 1 and self.end == 1:
                self.planet1.mass -= 0.1
                if self.o_start == self.planet2.owner:
                    self.planet2.mass += 0.1
                else:
                    self.planet2.mass -= 0.1
            elif self.begin == 1:
                self.planet1.mass -= 0.1
            elif self.end == 1:
                if self.o_start == self.planet2.owner:
                    self.planet2.mass += 0.1
                else:
                    self.planet2.mass -= 0.1


            if self.planet1.owner != self.owner:
                self.stop()

            if self.planet2.mass <= 0:
                self.capture()
            self.update()


        def capture(self):
            self.planet2.color = self.color
            self.planet2.owner = self.o_start
            self.planet2.level = 1
            self.planet2.r = 17
            self.planet2.mass = 1
            self.planet2.redraw()
            self.planet2.highlighting = 0
            canvas.delete(self.planet2.id1)

        def finish(self):
            canvas.delete(self.id)
            self.begin = 0
            self.end = 0
            lines.remove(self)


    def update(self):
        self.x1 = self.planet1.x + self.planet1.r * math.cos(self.an)
        self.y1 = self.planet1.y + self.planet1.r * math.sin(self.an)
        self.x2 = self.planet2.x - self.planet2.r * math.cos(self.an)
        self.y2 = self.planet2.y - self.planet2.r * math.sin(self.an)
        self.r = ((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2) ** 0.5
        self.redraw()


def click(event):
    """
    Эта функция реагирует на нажатие ллевой кнопкой мыши игроком, позволяет
    выделить планету, провести атаку, или сделать апгрейд

    """
    sec_click = 0
    space_click = 1
    i = 0
    allow = 1
    for i in planets:
        if i.highlighting == 1:
            sec_click = 1
            break

    if sec_click == 1:
        for j in planets:
            if ((event.x - j.x) ** 2 + (event.y - j.y) ** 2) <= j.r ** 2:

                for k in lines:
                    if k.planet1 == i:
                if i.mass <= 0:
                    allow = 0
                if allow == 1:
                    i.second_click(j)
                    space_click = 0
                    break
                allow = 1
        i.highlighting = 0
        canvas.delete(i.id1)
        if space_click == 1:
            for k in lines:
                if k.planet1 == i:
                    k.stop()
    else:
        for j in planets:
            if (((event.x - j.x) ** 2 + (event.y - j.y) ** 2) <= (j.r) ** 2) and (j.owner == 1):
                j.first_click()


def read_space_objects_data_from_file(input_filename):
    global aggressiveness
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """
    objects = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            object_type = line.split()[0].lower()
            if object_type == "planet":
                p = parse_planet_parameters(line)
                objects.append(p)
            else:
                aggressiveness = int(object_type)
    return objects


def parse_planet_parameters(line):
    """Считывает данные о планете из строки.
    Предполагается такая строка:
    Входная строка должна иметь слеюущий формат:
    Planet <масса> <x> <y> <пользователь> <уровень>

    Здесь (x, y) — координаты планеты.
    Пример строки:
    planet 10 500 400 1 2

    Параметры:

    **line** — строка с описание планеты.
    **planet** — объект планеты.
    """
    line = line.split()

    parameter_1 = int(line[1])
    parameter_2 = int(line[2])
    parameter_3 = int(line[3])
    parameter_4 = int(line[4])
    parameter_5 = int(line[5])
    return Planet(parameter_1, parameter_2, parameter_3, parameter_4, parameter_5)


class App():
    def __init__(self):
        self.root = Tkinter.Tk()
        button = Tkinter.Button(self.root, text = 'root quit', command=self.quit)
        button.pack()
        self.root.mainloop()

    def quit(self):
        self.root.destroy()


def II(me):
    '''Эта функция отвечает за поведение вражеских планет'''
    global planets, aggressiveness
    all_planets = []
    for i in planets:
        all_planets.append(i)
    my_planets = []
    other_planets = []
    enemy_planets = []
    neutral_planets = []
    my_planets_at = []
    player_planets = []
    allow = 1
    target = 0
    stopper = 0
    enemy_target = 0
    neutral_target = 0
    enemy_length = 5000
    neutral_length = 5000
    exit = 0
    attack_potential = 0
    maxmass = 0
    maxmass_p = 0
    for bl in range (10):
        for i in all_planets:
            if i.owner == me:
                if i.mass >= 25 * (2 ** i.level) and i.growing <= 0:
                    i.second_click(i)
                else:
                    if i.growing <= 0:
                        my_planets.append(i)
            else:
                other_planets.append(i)
                if i.owner == 0:
                    neutral_planets.append(i)
                else:
                    other_planets.append(i)
                    if i.owner == 0:
                        neutral_planets.append(i)
                    else:
                        enemy_planets.append(i)
            if len(my_planets) != 0 and len(other_planets) != 0:
                for i in my_planets:
                    attack_potential += i.mass
                if len(enemy_planets) != 0:
                    while exit <= len(enemy_planets):
                        for i in my_planets:
                            for j in enemy_planets:
                                if (i.x - j.x) ** 2 + (i.y - j.y) ** 2 <= enemy_length ** 2:
                                    enemy_length = ((i.x - j.x) ** 2 + (i.y - j.y) ** 2) ** 0.5
                                    target1 = j
                        if target1.mass + 3 < attack_potential:
                            enemy_target = target1
                            break
                        elif target1 in enemy_planets:
                            enemy_planets.remove(target1)
                            exit += 1
                        enemy_length = 5000
                if len(neutral_planets) != 0:
                    while exit <= len(neutral_planets):
                        for i in my_planets:
                            for j in neutral_planets:
                                if (i.x - j.x) ** 2 + (i.y - j.y) ** 2 <= neutral_length ** 2:
                                    neutral_length = ((i.x - j.x) ** 2 + (i.y - j.y) ** 2) ** 0.5
                                    target1 = j
                        if target1.mass + 3 < attack_potential:
                            neutral_target = target1
                            break
                        elif target1 in neutral_planets:
                            neutral_planets.remove(target1)
                            exit += 1
                        neutral_length = 5000
                if neutral_target == 0:
                    target = enemy_target
                elif enemy_target == 0:
                    target = neutral_target
                elif neutral_target == 0 and enemy_target == 0:
                    pass
                else:
                    if neutral_length * (1 + aggressiveness * 0.3) < enemy_length:
                        target = neutral_target
                    else:
                        target = enemy_target
                if target != 0:
                    for i in my_planets:
                        if i.mass > maxmass:
                            maxmass = i.mass
                            maxmass_p = i
                    maxmass = 500

                    one_attack_potential += maxmass_p.mass
                    if len(my_planets) == 0:
                        stopper = 1
                        break
                maxmass = 0
                if stopper == 0:
                    for i in my_planets_at:
                        for k in lines:
                            if k.planet1 == i:
                                k.stop()
                        if i.mass <= 0:
                            allow = 0
                        if allow == 1:
                            i.second_click(target)
                            if i in all_planets:
                                all_planets.remove(i)
                        allow = 1
                        if target in all_planets:
                            all_planets.remove(target)
                stopper = 0
            my_planets_at = []
            my_planets = []
            neutral_planets = []
            enemy_planets = []
            other_planets = []
            maxmass_p = 0
            target = 0
            enemy_target = 0
            neutral_target = 0


def fin():
    time.sleep(3)
    root.destroy()


def update():
    """Эта функия отвечает за обновление экрана"""
    global counter, flag_lose, flag_win
    player_planets = 0
    II_planets = 0
    if counter >= 200:
        counter = 0
        for i in range(2):
            II(i + 2)
    for i in lines:
        i.grow()
        i.redraw()
    for j in planets:
        j.grow()
        j.massupdate()
        if j.owner == 1:
            player_planets += 1
        if j.owner == 2 or j.owner == 3:
            II_planets += 1
    if player_planets == 0:
        canvas.create_text(1000, 500, text='YOU LOSE', fill='white', font="Times 60")
        root.after(10, fin)
    if II_planets == 0:
        canvas.create_text(1000, 500, text='YOU WIN', fill='white', font="Times 60")
        root.after(10, fin)
    counter += 1
    root.after(1, update)


def main(s0):
    global planets
    s = 'C:\Python\War_Of__Worlds\Maps/' + s0 + '.txt'
    planets = read_space_objects_data_from_file(s)
    canvas.bind('<Button-1>', click)
    update()


lets_play()



