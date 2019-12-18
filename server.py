# coding=utf-8
from tkinter import *
from random import randrange as rnd, choice
import tkinter as tk
import math
# from input_map import read_space_objects_data_from_file as read
import time
import socket
import pickle
import sys

lines = []
planets = []
counter = 0
aggressiveness = 0
flag_win = [0, 0]
flag_lose = 0
second_player = 0
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('', 8007))
serv_sock.listen(10)


def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb


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
        self.id = 0
        self.mass_limit = 0
        self.x = x
        self.y = y
        self.id1 = 0
        self.level = lvl
        self.text = 0
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

    def first_click(self):
        self.highlighting = 1

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
            self.growing -= 0.1

    def massupdate(self):
        if self.mass < 25 * (2 ** self.level):
            self.mass += self.level / 100


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
        self.id = 0
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
        self.id = 0

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
        self.planet2.highlighting = 0

    def finish(self):
        self.begin = 0
        self.end = 0
        lines.remove(self)

    def update(self):
        self.x1 = self.planet1.x + self.planet1.r * math.cos(self.an)
        self.y1 = self.planet1.y + self.planet1.r * math.sin(self.an)
        self.x2 = self.planet2.x - self.planet2.r * math.cos(self.an)
        self.y2 = self.planet2.y - self.planet2.r * math.sin(self.an)
        self.r = ((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2) ** 0.5

    def stop(self):
        if self.begin != 0:
            self.Num = self.count1
            self.begin = 0


def click_1(x, y):
    global planets, lines
    """
    Эта функция реагирует на нажатие ллевой кнопкой мыши игроком, позволяет
    выделить планету, провести атаку, или сделать апгрейд
    """
    sec_click = 0
    space_click = 1
    i = 0
    allow = 1
    for i in planets:
        if i.highlighting == 1 and i.owner == 1:
            sec_click = 1
            break
    if sec_click == 1:
        for j in planets:
            if ((x - j.x) ** 2 + (y - j.y) ** 2) <= j.r ** 2:
                for k in lines:
                    if k.planet1 == i:
                        k.stop()
                if i.mass <= 0:
                    allow = 0
                if allow == 1:
                    i.second_click(j)
                    space_click = 0
                    break
                allow = 1
        i.highlighting = 0
        if space_click == 1:
            for k in lines:
                if k.planet1 == i:
                    k.stop()
    else:
        for j in planets:
            if (((x - j.x) ** 2 + (y - j.y) ** 2) <= (j.r) ** 2) and (j.owner == 1):
                j.first_click()


def click_2(x, y):
    global planets, lines
    """
    Эта функция реагирует на нажатие ллевой кнопкой мыши игроком, позволяет
    выделить планету, провести атаку, или сделать апгрейд
    """
    sec_click = 0
    space_click = 1
    i = 0
    allow = 1
    for i in planets:
        if i.highlighting == 1 and i.owner == 2:
            sec_click = 1
            break
    if sec_click == 1:
        for j in planets:
            if ((x - j.x) ** 2 + (y - j.y) ** 2) <= j.r ** 2:
                for k in lines:
                    if k.planet1 == i:
                        k.stop()
                if i.mass <= 0:
                    allow = 0
                if allow == 1:
                    i.second_click(j)
                    space_click = 0
                    break
                allow = 1
        i.highlighting = 0
        if space_click == 1:
            for k in lines:
                if k.planet1 == i:
                    k.stop()
    else:
        for j in planets:
            if (((x - j.x) ** 2 + (y - j.y) ** 2) <= (j.r) ** 2) and (j.owner == 2):
                j.first_click()


def II(me):
    '''Эта функция отвечает за поведение вражеских планет'''
    global planets, aggressiveness, lines
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
    stopper = 0
    enemy_target = 0
    neutral_target = 0
    enemy_length = 5000
    neutral_length = 5000
    exit = 0
    attack_potential = 0
    maxmass = 0
    maxmass_p = 0
    for bl in range(10):
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


def update():
    while True:
        global rem_client_addr, second_player
        # Бесконечно обрабатываем входящие подключения
        client_sock, client_addr = serv_sock.accept()
        client_addr = client_addr[0:-1]
        try:
            if rem_client_addr != client_addr:
                second_player = 1
        except NameError:
            pass
        print(client_addr)
        rem_client_addr = client_addr
        while True:
            """Эта функия отвечает за обновление экрана"""
            global counter, planets, lines
            data = client_sock.recv(1000000)
            if not data:
                break
            data = pickle.loads(data)
            if data == 1:
                pass
            elif type(data[0]) == int:
                if data[2] == 1:
                    click_1(data[0], data[1])
                if data[2] == 2:
                    click_2(data[0], data[1])
            else:
                planets = data[0]
                lines = data[1]
                second_player = 0
            if counter >= 100:
                counter = 0
                II(3)
            for i in lines:
                i.grow()
            for j in planets:
                j.massupdate()
                j.grow()
            counter += 1
            client_sock.send(pickle.dumps([planets, lines, second_player], 2))
            second_player = 0
        client_sock.close()

update()
