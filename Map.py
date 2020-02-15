import requests
from pygame import Surface, image, Rect
import pygame
from io import BytesIO
from Widget import Widget, Application
from WEB_requests import LoadChunk


def generate_coord(x, y):
    print(y)
    mn = 1 if y > 0 else -1
    nm = -3.4 if y <= 0 else 0
    # Коменты не актуальны, кстати, надо будет сделать более точное размещение, но это только тогда, когда будет норм
    # зум, то есть завтра
    if round(abs(y)) == 0:
        return f"{x * 17.5},{1.7 * mn - nm}"
    elif round(abs(y)) == 1:  # 17.3
        return f"{x * 17.5},{19 * mn - nm}"
    elif round(abs(y)) == 2:  # 15.5
        return f"{x * 17.5},{34.5 * mn - nm}"
    elif round(abs(y)) == 3:  # 13.5
        return f"{x * 17.5},{47.75 * mn - nm}"
    elif round(abs(y)) == 4:  # 11.5
        return f"{x * 17.5},{58.28 * mn - nm}"
    elif round(abs(y)) == 5:  # 8
        return f"{x * 17.5},{66.4 * mn - nm}"
    elif round(abs(y)) == 6:  # 6.1
        return f"{x * 17.5},{72.53 * mn - nm}"
    elif round(abs(y)) == 7:  # 4.55
        return f"{x * 17.5},{77.095 * mn - nm}"
    elif round(abs(y)) == 8:  # 3.37
        return f"{x * 17.5},{80.52 * mn - nm}"
    elif round(abs(y)) == 9:  # ~2
        return f"{x * 17.5},{83 * mn - nm}"
    elif round(abs(y)) == 10:  #
        return f"{x * 17.5},{84.67715 * mn - nm}"
    elif round(abs(y)) != 5:  # 5.5
        return f"{x * 17.5},{64 * mn - nm}"
    else:
        return f"{x},{y * 16}"


def get_spn(y):
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
        self.map_image = Surface((100, 100))
        super().__init__(self.map_image, (0, 0))
        self.size_image = (400, 400)
        self.map = {}
        self.step = 10
        self.coord_ = list(pos)
        self.coord_lu = [22.00, 22.00]
        self.pressed = False
        self.last_pos = None
        self.test = False
        if self.test:
            print(self.rect)

    def get_pos(self, x, y):
        return int(x - self.coord_[0]), int(self.coord_[1] - y)

    def get_step(self):
        return self.step

    def move_at(self, x, y):
        if self.test:
            print(self.coord_, x, y)
        self.coord_[0] += x
        self.coord_[1] -= y
        if self.test:
            print(self.coord_)

    def load_map(self):
        step = self.step  # - self.app.zoom
        for y in range(-1, (self.rect.bottom - self.rect.y) // 500 + 1 + (
                1 if (self.rect.bottom - self.rect.y) % 500 != 0 else 0)):
            for x in range(-1, (self.rect.right - self.rect.x) // 500 + 1 + (
                    1 if (self.rect.right - self.rect.x) % 500 != 0 else 0)):
                coord_ = (self.coord_[0] + step * x, self.coord_[1] + step * y)
                ll = ','.join(map(str, coord_))
                if self.test:
                    print(ll)
                params = {
                    "ll": ll,
                    "spn": ",".join([str(step), str(step)]),
                    "l": "map",
                    'size': '500,500'
                }
                self.app.add_thread(LoadChunk('http://static-maps.yandex.ru/1.x/', params, self.add_chunk, ll))

    def generate_image(self):
        self.rect = Rect((0, 0), self.app.screen.get_size())
        image = Surface(self.app.get_size(1, 1))
        for key, val in self.map.items():
            if self.test:
                print(key, val)
                print(self.get_pos(*key), 'gg')
            # pygame.image.save(val, 'gg.png')
            image.blit(val, self.get_pos(*key))
        self.set_image(image)

    def add_chunk(self, request, coord):
        if request.status_code == 200:
            if self.test:
                print(coord[0] // self.step)
                print(coord[0] // self.step * self.size_image[0] + 10)
            coord = coord[0] // self.step * self.size_image[0], coord[1] // self.step * (self.size_image[1] + 0)
            self.map[coord] = image.load(BytesIO(request.content))
        else:
            raise Exception(f"Что-то пошло не так, проверьте соеденинение с интернетом. Ошибка: {request.status_code}.\n{request.url}")

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.pressed = True
            self.last_pos = event.pos
        if event.type == pygame.MOUSEMOTION and self.pressed and self.app.mouse_pressed(1) and self.get_active():
            self.move_at(self.last_pos[0] - event.pos[0], self.last_pos[1] - event.pos[1])
            self.last_pos = event.pos
            self.generate_image()
        if event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False


if __name__ == '__main__':
    api_server = "http://static-maps.yandex.ru/1.x/"
    print('generate')
    params = {
        "ll": '0.0,0.0',
        'spn': "10.0,10.0",
        "l": "sat",
        "z": "5",
        "size": "400,400"
    }

    app = Application((500, 500))
    map = Map((int(22.0 / 10 * 600), int(22.0 // 10 * 450 + 400)))
    app.add_widget(map)
    for y in range(-10, 11):
        for x in range(-10, 11):
            params["ll"] = generate_coord(x, y)
            params['spn'] = get_spn(y)
            map.add_chunk(requests.get(api_server, params=params), (x * 10, y * 10))
    map.generate_image()
    app.run()