import random

import requests
from pygame import Surface, image, Rect
import pygame
from io import BytesIO
from Widget import Widget, Application
from WEB_requests import LoadChunk


def generate_coord(x, y):
    mn = 1 if y > 0 else -1
    # Коменты не актуальны, кстати, надо будет сделать более точное размещение, но это только тогда, когда будет норм
    # зум, то есть завтра
    y = round(abs(y))
    x //= 10
    x_, y_ = x * 17.5, 0
    delt = [17.4, 15.9, 13.4, 10.7, 8.34, 6.27, 4.7, 3.48, 2.57, 1.87]
    if y > 0:  # 17.4
        y_ += delt[0] if y >= 10 else delt[0] * (y / 10)
    if y > 10:  # 15.9
        y_ += delt[1] if y >= 20 else delt[1] * ((y - 10) / 10)
    if y > 20:  # 13.4
        y_ += delt[2] if y >= 30 else delt[2] * ((y - 20) / 10)
    if y > 30:  # 10.7
        y_ += delt[3] if y >= 40 else delt[3] * ((y - 30) / 10)
    if y > 40:  # 8.34
        y_ += delt[4] if y >= 50 else delt[4] * ((y - 40) / 10)
    if y > 50:  # 6.27
        y_ += delt[5] if y >= 60 else delt[5] * ((y - 50) / 10)
    if y > 60:  # 4.7
        y_ += delt[6] if y >= 70 else delt[6] * ((y - 60) / 10)
    if y > 70:  # 3.48
        y_ += delt[7] if y >= 80 else delt[7] * ((y - 70) / 10)
    if y > 80:  # 2.57
        y_ += delt[8] if y >= 90 else delt[8] * ((y - 80) / 10)
    if y > 90:  # 1.87
        y_ += delt[9] if y >= 100 else delt[9] * ((y - 90) / 10)
    return f'{x_},{round(y_ * mn, 3)}'


def get_spn(y):
    # какято фигня
    if abs(y) <= 3:
        return f"{10},{10}"
    elif abs(y) == 4:
        return f"{7.5},{7.5}"
    elif abs(y) == 5:
        return f"{5},{5}"
    elif abs(y) in [6, 7]:
        return f"{3},{3}"
    elif abs(y) in [8, 9]:
        return f"{2},{2}"
    else:
        return f"{3},{3}"


class Map(Widget):
    def __init__(self, pos):
        """виджет карты на весь экран"""
        self.map_image = Surface((1000, 800))
        super().__init__(self.map_image, (0, 0), is_zooming=True, stock=False)
        self.size_image = (400, 400)
        self.map = {}
        self.step = 10
        self.coord_ = list(pos)
        self.coord_lu = [22.00, 22.00]
        self.pressed = False
        self.last_pos = None
        self.test = False
        self.size_chunk = (8230, 7905)
        self.mod = 'sat,skl'
        self.mods = None
        self.firstRender = True
        self.chunks = []
        # if self.test:
        # print(self.rect)

    def get_pos(self, x, y):
        return int(x - self.coord_[0]), int(self.coord_[1] - y)

    def add_mod(self, mod):
        """Ожидается RadioButtons чтобы получить режим карты"""
        self.mods = mod
        if self.update_mod():
            self.generate_image()
        self.mods.set_map(self)

    def update_mod(self):
        """обновляет режим карты если режим изменился возвращает True иначе False"""
        if self.mods is not None:
            if self.mods.get_choice() != self.mod and self.mods.get_choice() is not None:
                self.mod = self.mods.get_choice()
                self.map = {}
                self.generate_image()
            return self.mods.get_choice() != self.mod
        return False

    def get_step(self):
        return self.step

    def move_at(self, x, y):
        if self.test:
            print(self.coord_, x, y)
        self.coord_[0] += x
        self.coord_[0] %= 8230
        self.coord_[1] -= y
        if self.coord_[1] > 7905:
            self.coord_[1] = 7905
        elif self.coord_[1] < 550:
            self.coord_[1] = 550
        if self.test:
            print(self.coord_)

    def load_map(self, x, y):
        api_server = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": generate_coord((x - 10) * 10, (y - 10) * 10),
            'spn': get_spn(y - 10),
            "l": self.mod,
            "z": "1",
            "size": "400,400"
        }
        self.app.add_thread(LoadChunk(api_server, params, self.add_chunk, (x * 10, y * 10, self.mod)))

    def get_point(self, coord):
        pass

    def generate_image(self, load_new_chunks=True):
        self.rect = Rect((0, 0), self.app.screen.get_size())
        res = []
        coord = self.coord_[:]
        size = self.app.screen.get_size()
        count = 0
        map_ = self.map.copy()
        # print("coord:", coord[0] // self.size_image[0], coord[1] // self.size_image[1])
        for y in range(coord[1] // self.size_image[1] - 2, (coord[1] + size[1]) // self.size_image[1]):
            for x in range(coord[0] // self.size_image[0] - 1, (coord[0] + size[0]) // self.size_image[0] + 1):
                x %= 21
                y %= 21
                try:
                    # print(x, y)
                    res.append(((x * self.size_image[0], y * self.size_image[1]), map_[(x * self.size_image[0], y * self.size_image[1])]))
                    count += 1
                except Exception:
                    if load_new_chunks:
                        self.load_map(x, y)
        # print(count)
        self.chunks = res
        self.draw_chunks()

    def draw_chunks(self):
        image = Surface(self.app.get_size(1, 1))
        for key, val in self.chunks:
            if self.test:
                print(key, val)
                print(self.get_pos(*key), 'gg')
            # pygame.image.save(val, 'gg.png')
            image.blit(val, self.get_pos(*key))
            image.blit(val, (self.get_pos(*key)[0] + 8230, self.get_pos(*key)[1]))
        self.set_image(image)

    def add_chunk(self, request, coord):
        if request.status_code == 200 and self.mod == coord[2]:
            # if self.test:
            # print(coord[0] // self.step)
            # print(coord[0] // self.step * self.size_image[0] + 10)
            coord = coord[0] // self.step * self.size_image[0], coord[1] // self.step * (self.size_image[1] + 0)
            self.map[coord] = image.load(BytesIO(request.content))
            self.generate_image(False)
        else:
            raise Exception(
                f"Что-то пошло не так, проверьте соеденинение с интернетом. Ошибка: {request.status_code}.\n{request.url}")

    def update(self, event):
        if self.firstRender:
            self.firstRender = False
            self.generate_image()
        if self.update_mod():
            self.generate_image()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.pressed = True
            self.last_pos = event.pos
        if event.type == pygame.MOUSEMOTION and self.pressed and self.app.mouse_pressed(1) and self.get_active():
            self.move_at(self.last_pos[0] - event.pos[0], self.last_pos[1] - event.pos[1])
            self.last_pos = event.pos
            # if self.test:
            # print(self.coord_)
            self.generate_image()
        if event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
            # print("point:", self.coord_[0] + event.pos[0], self.coord_[1] + event.pos[1])


if __name__ == '__main__':
    for y in range(-100, 101, 10):
        print(generate_coord(0, y))
