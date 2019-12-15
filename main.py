from random import randrange as rnd, choice
import tkinter as tk
import math
#from input_map import read_space_objects_data_from_file as read
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
aggressiveness = 0


def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb


class Planet:
    '''Этот класс отвечает за создание и отрисовку планет,
    их динамическое цветовое отображение'''
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
            start = self.owner
            end = other.owner
            mass = self.mass
            color = self.color
            l = Line(self, other, start, mass, color)
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
    '''Этот класс овечает за отрисовку линий,
    с помощью которых атакуют планеты и пресчет масс'''
    def __init__(self,
                 p1,
                 p2,
                 start,
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
        self.color = color
        self.o_start = start
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
        if self.planet2.mass <= 0:
            self.capture()

    def capture(self):
        self.planet2.color = self.color
        self.planet2.owner = self.o_start
        self.planet2.level = 1
        self.planet2.r = 17
        self.planet2.mass = 1
        self.planet2.redraw()
        self.planet2.highlighting = 0
        canvas.delete(self.planet2.id1)

    def stop(self):
        canvas.delete(self.id)
        self.begin = 0
        self.end = 0
        lines.remove(self)


def click(event):
    '''Эта функция реагирует на нажатие ллевой кнопкой мыши игроком, позволяет
    выделить планету, провести атаку, или сделать апгрейд'''
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
                    if k.planet1 == i:
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


def read_space_objects_data_from_file(input_filename):
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
                print("Unknown space object")
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
    allow = 1
    target = 0
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
                    else:
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
                    else:
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
            for i in my_planets:
                if i.mass > maxmass:
                    maxmass = i.mass
                    maxmass_p = i
            maxmass = 500
            my_planets.remove(maxmass_p)
            my_planets_at.append(maxmass_p)
            one_attack_potential = maxmass_p.mass
            while target.mass + 3 >= one_attack_potential:
                for i in my_planets:
                    if i.mass <= maxmass:
                        maxmass = i.mass
                        maxmass_p = i
                if maxmass_p in my_planets:
                    my_planets.remove(maxmass_p)
                my_planets_at.append(maxmass_p)
                maxmass = 500
                one_attack_potential += maxmass_p.mass
                if len(my_planets) == 0:
                    break
            maxmass = 0
            if target != 0:
                for i in my_planets_at:
                    for k in lines:
                        if k.planet1 == i:
                            allow = 0
                    if i.mass <= 0:
                        allow = 0
                    if allow == 1:
                        i.second_click(target)
                        if i in all_planets:
                            all_planets.remove(i)
                    allow = 1
                    if target in all_planets:
                        all_planets.remove(target)
            my_planets_at = []
            my_planets = []
            neutral_planets = []
            enemy_planets = []
            other_planets = []
            maxmass_p = 0
            target = 0
            enemy_target = 0
            neutral_target = 0


def update():
    '''Эта функия отвечает за обновление экрана'''
    global counter
    if counter >= 500:
        counter = 0
        for i in range(2):
            II(i + 2)
    for i in lines:
        i.grow()
        i.redraw()
    for j in planets:
        j.grow()
        j.massupdate()
    counter += 1
    root.after(10, update)

def main():
    global planets
    planets = read_space_objects_data_from_file('Example.txt')
    canvas.bind('<Button-1>', click)
    update()

main()

root.mainloop()
