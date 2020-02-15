from pygame import Surface, Rect, image
from io import BytesIO
from Widget import Widget
from WEB_requests import LoadChunk


class Map(Widget):
    def __init__(self):
        self.map_image = Surface((100, 100))
        super().__init__(self.map_image, (0, 0))
        self.map = {}
        self.step = 10
        self.coord = [22.00, 22.00]
        self.coord_lu = self.coord[:]
        print(self.rect)

    def load_map(self):
        step = self.step  # - self.app.zoom
        for y in range(-1, (self.rect.bottom - self.rect.y) // 500 + 1 + (
        1 if (self.rect.bottom - self.rect.y) % 500 != 0 else 0)):
            for x in range(-1, (self.rect.right - self.rect.x) // 500 + 1 + (
            1 if (self.rect.right - self.rect.x) % 500 != 0 else 0)):
                coord = (self.coord[0] + step * x, self.coord[1] + step * y)
                ll = ','.join(map(str, coord))
                print(ll)
                params = {
                    "ll": ll,
                    "spn": ",".join([str(step), str(step)]),
                    "l": "map",
                    'size': '500,500'
                }
                self.app.add_thread(LoadChunk('http://static-maps.yandex.ru/1.x/', params, self.add_chunk, ll))

    def generate_image(self):
        image = Surface(self.app.screen.get_size())


    def add_chunk(self, request, coord):
        if request
        self.map[coord] = image.load(BytesIO(request.content))

    def update(self, event):
        if self.map == {}:
            self.load_map()


Map().add_chunk()
