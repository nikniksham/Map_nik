from pygame import Surface
from pygame.transform import *
import pygame
import os
from pygame.draw import *
from win32api import GetSystemMetrics
from ctypes import *
# Импортируем всё необходимое


def get_lang():
    user32 = windll.user32
    hwnd = user32.GetForegroundWindow()
    threadID = user32.GetWindowThreadProcessId(hwnd, None)
    return 'ru' if user32.GetKeyboardLayout(threadID) == 68748313 else 'eng'


# Эти строки мазахизма - русская раскладка
rus_text = {'`': 'ё', 'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г',
            'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в',
            'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж', "'": 'э',
            'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б',
            '.': 'ю'}
good_symbols = ['`', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', 'a', 's', 'd', 'f',
                'g', 'h', 'j', 'k', 'l', ';', "'", 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '0',
                '1', '2', '3', '4', '5', '6', '7', '8', '9']


def load_image(name):
    """Открытие изображений"""
    fullname = os.path.join('data', name)
    # Проверка на то, что изображение по этому пути существует
    if os.path.isfile(fullname):
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        return image
    raise Exception(f'Изображение по пути {fullname} не существует')


def check_image(image, help_name=None):
    """Проверка картинки, или путя к ней
    Есть 2 параметра: 1 обязательный - путь к картинке, 2 - необязательный, это имя, нужное для отладки"""
    # 2 параметра - картинка, или путь к ней, а так же её имя, нужное для отладки
    if type(image) != pygame.Surface:
        if type(image) == str:
            image = load_image(image)
        else:
            if help_name is None:
                help_name = image
            raise Exception(f'Неподходяций формат, заданый картинке {help_name}')
    return image


class ScreenSize:
    def __init__(self):
        self.size_screen = [GetSystemMetrics(0), GetSystemMetrics(1)]

    def get_size(self, x, y):
        return [self.size_screen[0] * x, self.size_screen[1] * y]


size_screen = ScreenSize()


class Smooth:
    """Создаёт скруглёное Изображение"""
    def __init__(self, pos, size, smooth, color=(255, 255, 255)):
        """pos - левая верхняя точка
        size - размер всего изображения
        smooth - радиус закругления
        color - цвет изображения"""
        # Радиус закругления
        self.smooth = 0
        # Изображение
        self.image = pygame.Surface((10, 10))
        # Прямоугольник изображения
        self.rect = pygame.Rect(0, 0, 0, 0)
        # Задаём позицию
        self.set_pos(pos)
        # Задаём размер кнопки
        self.set_size(size)
        # Задаём радиус закругления
        self.set_smooth(smooth)
        # Задаём цвет
        self.color = color
        # Режим отладки выводит отладочную иномацию
        self.test = False

    def set_pos(self, pos):
        """Задать позицию"""
        if len(pos) != 2:
            raise Exception(f"pos is not pos")
        self.rect.x, self.rect.y = pos

    def set_size(self, size):
        """Задать размер"""
        if len(size) != 2:
            raise Exception(f"size is not size")
        self.rect.width, self.rect.height = size
        self.image = pygame.Surface(size)

    def set_smooth(self, smooth):
        """задать радиус скругления"""
        if type(smooth) != int:
            raise TypeError(f"type {smooth} != type int")
        if min(self.rect.width, self.rect.height) // 2 >= smooth:
            self.smooth = smooth
        else:
            raise Exception(f"Smooth more than max smooth")

    def set_color(self, color):
        """Задать цвет RGB"""
        if len(color) != 3:
            raise Exception(f"{color} is not color.")
        self.color = color

    def generate_smooth(self):
        """сгенерировать изображение
        возвращает готовое изображение"""
        self.image.set_colorkey((0, 0, 0))
        if self.test:
            print('Smooth Image')
            print(self.smooth, self.smooth)
            print(self.rect.right - self.smooth, self.smooth)
            print(self.smooth, self.rect.bottom - self.smooth)
            print(self.rect.right - self.smooth, self.rect.bottom - self.smooth)
            print((0, self.smooth), (self.rect.right, self.rect.height - self.smooth * 2))
            print((self.smooth, 0), (self.rect.right - self.smooth * 2, self.rect.bottom))
        # левый верхний круг
        circle(self.image, self.color, (self.smooth, self.smooth), self.smooth)
        # правый верхний круг
        circle(self.image, self.color, (self.rect.right - self.smooth, self.smooth), self.smooth)
        # левый нижний круг
        circle(self.image, self.color, (self.smooth, self.rect.bottom - self.smooth), self.smooth)
        # правый нижний круг
        circle(self.image, self.color, (self.rect.right - self.smooth, self.rect.bottom - self.smooth), self.smooth)
        # горизонтальный прямоугольник
        rect(self.image, self.color, ((0, self.smooth), (self.rect.right, self.rect.height - self.smooth * 2)))
        # вертикальный прямоугольник
        rect(self.image, self.color, ((self.smooth, 0), (self.rect.right - self.smooth * 2, self.rect.bottom)))
        return self.image


class TextBox(pygame.sprite.Sprite):
    """Создаёт текст"""
    def __init__(self, size_pixel, text, color=(0, 0, 0)):
        """size_pixel - размер текста в пикселях
        text - текст
        color - цвет текста"""
        pygame.sprite.Sprite.__init__(self)
        # текст
        self.text = ''
        # размер шрифта
        self.font_size = 0
        # цвет шрифта
        self.color = (0, 0, 0)
        # изображение
        self.image = pygame.Surface((10, 10))
        # задаём размер шрифта
        self.set_font_size(size_pixel)
        # задаём текст
        self.set_text(text)
        # задаём цвет
        self.set_color(color)
        # инициализируем пугаме текст
        pygame.font.init()
        # задаём шрифт
        self.font = pygame.font.Font('data/Font/NeogreyMedium.otf', self.font_size)

    def set_font_size(self, size_pixels):
        """Задать размер текста в пикселях"""
        if type(size_pixels) not in [int, float]:
            raise TypeError(f"type {type(size_pixels)} not in [int, float]")
        self.font_size = int(size_pixels)

    def set_text(self, text):
        """Задать текст"""
        if type(text) != str:
            raise TypeError(f"type {type(text)} != type str")
        self.text = text

    def set_color(self, color):
        """Задать цвет RGB"""
        if len(color) != 3:
            raise Exception(f"{color} is not color.")
        self.color = color

    def get_image(self):
        """Получить изображение с текстом"""
        self.image = self.font.render(self.text, False, self.color)
        return self.image


class Widgets:
    def __init__(self, screen):
        """Создаём список, в котором будут кнопки, которые будут обновляться"""
        self.screen = screen
        self.widgets = []

    def add_widget(self, widget):
        """Добавление кнопок в список"""
        if widget not in self.widgets:
            self.widgets.append(widget)
        else:
            raise Exception('Такая кнопка уже есть в списке обновления')

    def remove_widget(self, widget):
        """Удаление кнопок из списка"""
        if widget in self.widgets:
            self.widgets.remove(widget)
        else:
            raise Exception('Такой кнопки нет в списке обновления')

    def get_screen(self):
        """Возвращение screen"""
        return self.screen

    def update(self):
        """Обновление кнопок"""
        for widget in self.widgets:
            widget.update(self.screen)


class Widget:
    def __init__(self, image, action, coord):
        """Дочерний класс всех виджетов, в который передаются 3 обязательных параметра - изображение,
        действие и координаты соответственно"""
        self.image = image
        self.action = action
        self.active = False
        self.coord = coord
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.coord

    def set_coord(self, new_coord):
        """Изменение старых координат на новые"""
        self.coord = new_coord

    def get_coord(self):
        """Возвращает координаты"""
        return self.coord

    def set_image(self, new_image):
        """Изменяет старое изображение на новое"""
        self.image = new_image

    def set_action(self, new_action):
        """Изменяет старое действие на новое"""
        self.action = new_action

    def get_active(self):
        """Возращает параметр активности"""
        return self.active

    def set_active(self, active):
        """Задаёт активность виджету"""
        self.active = active


class Button(Widget):
    def __init__(self, image_inactive, image_active, action, coord):
        """Загрузка картинок - inactive_image, active_image"""
        self.image_inactive = check_image(image_inactive, 'image_inactive')
        self.image_active = check_image(image_active, 'image_active')
        self.action = action
        super().__init__(self.image_inactive, self.action, coord)

    def update(self, *args):
        """Обновление стандартной кнопки"""


class TextWidget(Widget):
    def __init__(self, image, coord):
        if image is None:
            self.image = Smooth((0, 0), size_screen.get_size(0.3, 0.05), 20, (200, 200, 200)).generate_smooth()
        else:
            self.image = check_image(image, 'image_text_widget')
        self.action = self.write_text
        self.text = ''
        super().__init__(self.image, self.action, coord)

    def write_text(self, event, space, backspace):
        """Функция написания текста в виджете TextWidget"""
        # Получение имени клавиши, если в программе выбран язык - английский, если выбран русский, то
        # подключается словарь "мазахиста"
        if not space and not backspace and event is not None:
            key_name = pygame.key.name(event.key)
            if key_name == 'return':
                self.set_active(False)
                return
            if key_name in good_symbols:
                # Проверка раскладки
                if get_lang() == 'eng':
                    self.text += key_name
                if get_lang() == 'ru':
                    if key_name in list(rus_text.keys()):
                        self.text += rus_text[key_name]
                    else:
                        self.text += key_name
        if space:
            self.text += ' '
        if backspace:
            if len(self.text) >= 0:
                self.text = self.text[:-1]

    def get_normal_text(self):
        """Эта функция возвращает текст для вывода"""
        return self.text

    def remove_text(self):
        """Эта функция удаляет весь текст из запроса"""
        self.text = ''

    def set_text(self, text):
        """Эта функция задаёт текст из переменной text"""
        self.text = text

    def update(self, *args):
        """Обновление текстового виджета"""
        screen = args[0]
        image = Smooth((0, 0), size_screen.get_size(0.3, 0.05), 20, (200, 200, 200)).generate_smooth()
        text = TextBox(size_screen.get_size(0.3, 0.035)[1], self.get_normal_text()).get_image()
        image.blit(text, [10, 0], ((text.get_width() - size_screen.get_size(0.24, 0)[0], 0), size_screen.get_size(0.24, 0.05)))
        self.image = image
        if self.get_active():
            # Если виджет активен, то мы делаем проверку на нажатие в любой другой точке программы, и делаем
            # виджет неактивным, если куда либо нажали ещё
            if not self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
                self.set_active(False)
                return
            # self.write_text()
        else:
            # Если виджет неактивен, то мы делаем проверку по его нажатию, и делаем активным, если на него нажали
            if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
                self.set_active(True)
        screen.blit(self.image, self.get_coord())

pygame.init()
FONT_STYLE = 'NeogreyMedium.otf'


def scale_to(image, size):
    return scale(image, size)


def create_text(text, size, color):
    font_type = pygame.font.Font(FONT_STYLE, size)
    return font_type.render(text, True, color)


class Application:
    # создание экрана
    def set_screen(self, size, full_screen=False):
        # экран
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN if full_screen else pygame.RESIZABLE)
        self.screen.fill(self.fill_color)
        # развёрнут на весь экран
        self.full_screen = full_screen
        # размер экрана
        self.size_screen = size
        #  ширина и высота
        self.widht, self.height = size

    def __init__(self, size_screen, fill_color=(0, 0, 0), full_screen=False):
        # создание экрана
        self.fill_color = fill_color
        self.set_screen(size_screen, full_screen)
        # нажатые клавиши клавиатуры
        self.pressed_key = []
        # нажатые клавиши мыши
        self.pressed_mouse_button = []
        # виджеты ключь=слой значение [виджеты]
        self.widgets = {}
        self.index_layers = []
        # аудио байлы
        self.audios = []
        # события функции
        self.events = []
        # анимационные виджеты
        self.animations = []
        # часы для граничения FPS
        self.clock = pygame.time.Clock()
        # количество кадров в секунду 0 - неограничено
        self.FPS = 80
        # приложение работает
        self.running = True
        # картинка мыши если None то обычная мышь
        self.mouse_image = None
        # список картинок мыши
        self.mouse_images = []
        self.mouse_rect = pygame.Rect(0, 0, 0, 0)

    # получить FPS
    def get_fps(self):
        return self.FPS

    # устатвить FPS 0 - неограничено
    def set_fps(self, count_fps):
        # возвращает True если установилость, False если не установилось
        if count_fps >= 0:
            self.FPS = count_fps
            return True
        return False

    # получить виджеты
    def get_widgets(self, layer=None, reverse=False):
        # получить виджеты с ключом слой
        if layer is not None:
            return self.widgets[layer]
        else:
            res = []
            keys = sorted(self.widgets.keys(), reverse=reverse)
            for key in keys:
                res += self.widgets[key]
            return res

    # добавить виджеты
    def add_widget(self, widget, layer=1):
        # добавить виджет на экран на слой=layer если не получается то return False
        if issubclass(type(widget), Widget):
            widget.set_application(self)
            widget.set_position(self.widht, self.height)
            if layer in self.widgets:
                if widget not in self.widgets[layer]:
                    self.widgets[layer].append(widget)
            else:
                self.widgets[layer] = [widget]
            return True
        return False

    def remove_widget(self, widget):
        for layer in self.get_layers():
            if widget in self.widgets[layer]:
                self.widgets[layer].remove(widget)
                return True
        return False

    # получить слои
    def get_layers(self):
        # получить список слоёв
        res = list(self.widgets.keys())
        res.sort()
        return res

    # получить аудио файлы
    def get_audios(self):
        # получить список аудиофайлов
        return self.audios

    # добавить аудио файлы
    def add_audio(self, audio):
        # добавить аудиофайл если не получается, то return False
        if issubclass(audio, Audio):
            self.audios.append(audio)
            return True
        return False

    # удалить аудиофайлы
    def remove_audio(self, audio):
        # удаляем аудиофайл, если не получается, то return False
        if audio in self.audios:
            self.audios.remove(audio)
            return True
        return False

    # добавить ивент
    def add_event(self, event):
        # добавляем событие выполняется каждую итерацию
        if event not in self.events:
            self.events.append(event)

    def remove_event(self, event):
        if event in self.events:
            self.events.remove(event)
            return True
        return False

    # получить размер экрана
    def get_size_screen(self):
        # получить размер экрана
        return self.size_screen

    def get_width(self):
        # получить ширину экрана
        return self.widht

    def get_height(self):
        # получить высоту экрана
        return self.height

    def get_full_screen(self):
        # получить развёрнуто на полный экран или нет
        return self.full_screen

    def quit(self):
        # выполняется при закрытии приложения
        pass

    def load_mouse_image(self, file):
        image = load_image(file, (255, 255, 255))
        self.mouse_images.append(image)

    def set_mouse_image(self, index):
        # установить картинку мыши из списка картинок мыши
        pygame.mouse.set_visible(False)
        self.mouse_image = self.mouse_images[index]
        self.mouse_rect = self.mouse_image.get_rect()

    def set_mouse_normal(self):
        # вернуть видимость мыши
        pygame.mouse.set_visible(True)
        self.mouse_image = None

    #
    # не лезь оно тебя сожрёт
    # внутреняя логика
    #
    def draw_mouse(self):
        # отрисовка мыши
        if self.mouse_image is not None:
            self.mouse_rect.x, self.mouse_rect.y = pygame.mouse.get_pos()
            self.screen.blit(self.mouse_image, self.mouse_rect)

    def update_screen(self, width, height):
        self.set_screen((width, height), self.get_full_screen())
        for widget in self.get_widgets():
            widget.set_position(width, height)

    # main loop
    def run(self):
        # основной цикл
        while self.running:
            # обробатываем события
            for event in pygame.event.get():
                # событие закрытия
                if event.type == pygame.QUIT:
                    self.running = False
                    return self.quit()
                if event.type == pygame.VIDEORESIZE:
                    width, height = event.w, event.h
                    self.set_screen((width, height), self.get_full_screen())
                    for widget in self.get_widgets():
                        widget.set_position(width, height)
                if event.type == pygame.MOUSEMOTION:
                    self.set_active_widgets(event)
                # событие нажатия клавиши мыши
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pressed_mouse_button.append(event.button)
                # событие нажатия клавиши клавиатуры
                if event.type == pygame.KEYDOWN:
                    self.pressed_key.append(event.key)
                    self.get_key_pressed_event(event)
                # событие отжатия клавиши мыши
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button in self.pressed_mouse_button:
                        self.pressed_mouse_button.remove(event.button)
                    self.mouse_key_up_event(event)
                # событие отжатия клавиши клавиатуры
                if event.type == pygame.KEYUP:
                    if event.key in self.pressed_key:
                        self.pressed_key.remove(event.key)
                    self.key_up_event(event)
            # обработка функций
            for funk in self.events:
                funk()
            # отрисовка экрана
            for widget in self.get_widgets():
                self.render(widget)
            # отрисовка мыши
            self.draw_mouse()
            # обновление экрана
            pygame.display.flip()
            if self.FPS != 0:
                self.clock.tick(self.FPS)
            else:
                self.clock.tick()
            self.screen.fill(self.fill_color)
        if not self.running:
            return self.quit()

    # отрисовка экрана
    def render(self, widget):
        if issubclass(type(widget), AnimationWidgets):
            if self.FPS != 0:
                widget.update(self.FPS)
            elif self.clock.get_fps() != 0:
                widget.update(self.clock.get_fps())
            self.screen.blit(widget.get_surface(), widget.get_rect())
        elif issubclass(type(widget), Widget):
            self.screen.blit(widget.get_surface(), widget.get_rect())

    # обработчик событий мыши
    def set_active_widgets(self, event):
        pos = event.pos
        good = False
        for widget in self.get_widgets(reverse=True):
            if good:
                widget.active = False
            else:
                widget.set_active(pos)
                if widget.get_active():
                    good = True

    def mouse_key_up_event(self, event):
        # asd
        if event.button == 1:
            self.on_click(event)
        else:
            self.mouse_event(event)

    # обработчик всех событий мыши кроме нажатия левой кнопкой мыши
    def mouse_event(self, event):
        if event.button in [4, 5]:
            for widget in self.get_widgets(reverse=True):
                if widget.get_active() and widget.get_is_zooming():
                    widget.zoom_update(event)
        else:
            for widget in self.get_widgets(reverse=True):
                if widget.get_active():
                    widget.update(event)

    # обрабатывает нажатие левой кнопкой мыши
    def on_click(self, event):
        for widget in self.get_widgets(reverse=True):
            if widget.get_active():
                # print(widget.rect)
                widget.update(event)

    # проверить нажата ли кнопка мыши
    def mouse_pressed(self, number_mouse):
        return number_mouse in self.pressed_mouse_button

    # получить нажатые кнопки
    def get_pressed_mouse(self):
        return self.pressed_mouse_button

    #
    # работа с клавиатурой
    #
    # получает события клавиатуры
    def get_key_pressed_event(self, event):
        self.key_pressed_event(event)

    # события клавиатуры
    def key_pressed_event(self, event):
        for widget in self.get_widgets(reverse=True):
            if widget.get_active():
                widget.update(event)

    # проверить нажата ли кнопка клавиатуры
    def key_pressed(self, key):
        return key in self.pressed_key

    def key_up_event(self, event):
        for widget in self.get_widgets(reverse=True):
            if widget.get_active():
                widget.update(event)

    # получить список нажатых кнопок
    def get_pressed_key(self):
        return self.pressed_key


class Widget:
    def __init__(self, surfaces, coord, active=False, is_zooming=False, zoom=1, max_zoom=1, min_zoom=0.15,
                 is_scrolling_x=False, is_scrolling_y=False, is_scroll_line_x=False, is_scroll_line_y=False, scroll_x=0,
                 scroll_y=0, size=None, stock=True):        # размер экрана
        self.size = size
        # зум
        self.zoom = zoom
        self.stock = stock
        # скролл по y
        self.scroll_y = scroll_y
        # скролл по x
        self.scroll_x = scroll_x
        # скролимый по x
        self.is_scrolling_x = is_scrolling_x
        # скролимый по x иил нет
        self.is_scrolling_y = is_scrolling_y
        # программа
        self.app = None
        self.start_zoom = zoom
        # оригинальное изоьражение
        res_surfaces = []
        if type(surfaces) == str:
            res_surfaces.append(load_image(surfaces).copy())
        elif type(surfaces) == Surface:
            res_surfaces = [surfaces]
        else:
            for surface in surfaces:
                if type(surface) == str:
                    res_surfaces.append(load_image(surface).copy())
                else:
                    res_surfaces.append(surface)
        self.images_orig = res_surfaces[:]
        self.set_image(self.images_orig[0])
        # рект
        self.rect = self.image.get_rect()
        # коорданиаты
        self.coord = coord
        self.rect.x, self.rect.y = coord
        # активени или нет
        self.active = active
        # зумируемый
        self.is_zooming = is_zooming
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        # есть скрол лента по x или нет
        self.is_scroll_line_x = is_scroll_line_x and is_scrolling_x
        # есть скрол лента по y или нет
        self.is_scroll_line_y = is_scroll_line_y and is_scrolling_y

    def set_image(self, image):
        self.image_orig = image
        self.image = self.image_orig
        if self.size is not None:
            self.image = scale_to(self.image, self.size)
        if self.app is not None:
            self.set_position(self.app.get_width(), self.app.get_height())
        if self.stock:
            self.zoom = self.start_zoom
        if self.zoom != 1:
            self.set_zoom(zoom=self.zoom)

    # пересчитать позицию
    def set_position(self, w, h):
        w_, h_ = self.coord
        if w_ < 0:
            self.rect.right = w + w_
        else:
            self.rect.x = w_
        if h_ < 0:
            self.rect.bottom = h + h_
        else:
            self.rect.y = h_

    # используется в приложении или нет
    def in_application(self):
        return True if self.app is not None else False

    # задать приложение в котором используется
    def set_application(self, app):
        self.app = app

    def get_application(self):
        return self.app

    # получить зумиреумый
    def get_is_zooming(self):
        return self.is_zooming

    # получить зум
    def get_zoom(self):
        # получить зум
        if self.is_zooming:
            return self.zoom
        return 1

    def zoom_update(self, event):
        if self.rect.collidepoint(event.pos):
            if event.button == 5:
                self.zoom += self.zoom * 0.1
                if self.zoom > self.max_zoom:
                    self.zoom = self.max_zoom
            elif event.button == 4:
                self.zoom -= self.zoom * 0.1
                if self.zoom < self.min_zoom:
                    self.zoom = self.min_zoom
            self.set_zoom(self.zoom)

    def set_zoom(self, zoom):
        w = self.image_orig.get_width() * zoom
        h = self.image_orig.get_height() * zoom
        w_, h_ = self.image_orig.get_size()
        scroll_x = -self.scroll_x if self.is_scrolling_x else -((w_ - w) / 2)
        scroll_y = -self.scroll_y if self.is_scrolling_y else -((h_ - h) / 2)
        self.image = Surface((w, h))
        self.image.blit(self.image_orig, (scroll_x, scroll_y))
        self.image = scale(self.image, (self.image_orig.get_width(), self.image_orig.get_height()))
        if self.size is not None:
            self.image = scale_to(self.image, self.size)
        self.rect = self.image.get_rect()
        if self.app is not None:
            self.set_position(self.app.get_width(), self.app.get_height())

    # получить скролимый по x
    def get_is_scrolling_x(self):
        return self.is_scrolling_x

    # получить скролимый по y
    def get_is_scrolling_y(self):
        return self.is_scrolling_y

    # получить скрол по x
    def get_scroll_x(self):
        # скрол по x если нельзя, то return False
        if self.is_scrolling_x:
            return self.scroll_x
        return False

    # полчучить скрол по y
    def get_scroll_y(self):
        # скрол по y если нельзя, то return False
        if self.is_scrolling_y:
            return self.scroll_y
        return False

    # проскролить по x
    def set_scroll_x(self, add_num):
        # добавить скрол по x, иначе return False
        if self.is_scrolling_x:
            self.scroll_x += add_num
            return True
        return False

    # проскролить по y
    def set_scroll_y(self, add_num):
        # добавить скрол по y, иначе return False
        if self.is_scrolling_x:
            self.scroll_x += add_num
            return True
        return False

    # обновить виджет
    def update(self, event):
        pass

    # получить активен ли виджет
    def get_active(self):
        return self.active

    # устнавить активным виджет
    def set_active(self, pos):
        self.active = self.rect.collidepoint(pos)

    # получить эзображение
    def get_surface(self):
        return self.image

    # получить координаты
    def get_coord(self):
        return self.rect.x, self.rect.y

    # поллучить Rect
    def get_rect(self):
        return self.rect


class Audio:
    pass


class Button(Widget):
    def __init__(self, surfaces, coord, function, active=False, is_zooming=False, zoom=1, max_zoom=1, min_zoom=0.15,
                 is_scrolling_x=False, is_scrolling_y=False, is_scroll_line_x=False, is_scroll_line_y=False, scroll_x=0,
                 scroll_y=0, push=False):
        super().__init__(surfaces, coord, active, is_zooming, zoom, max_zoom, min_zoom, is_scrolling_x, is_scrolling_y,
                         is_scroll_line_x, is_scroll_line_y, scroll_x, scroll_y)
        self.pressed = False
        self.function = function
        self.push = push

    def set_active(self, pos):
        self.active = self.rect.collidepoint(pos)

    def get_pressed(self):
        return self.pressed

    def get_surface(self):
        # print(self.active)
        if self.active or self.pressed:
            return self.images_orig[1]
        else:
            return self.images_orig[0]

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if not self.push:
                    self.pressed = not self.pressed
                self.set_image(self.images_orig[self.pressed])
                self.function(self)


class AnimationWidgets(Widget):
    def __init__(self, surfaces, coord, sec, active=False, is_zooming=False, zoom=1, max_zoom=1, min_zoom=0.15,
                 is_scrolling_x=False, is_scrolling_y=False, is_scroll_line_x=False, is_scroll_line_y=False, scroll_x=0,
                 scroll_y=0):
        super().__init__(surfaces, coord, active, is_zooming, zoom, max_zoom, min_zoom, is_scrolling_x, is_scrolling_y,
                         is_scroll_line_x, is_scroll_line_y, scroll_x, scroll_y)
        self.sec = sec
        self.tick = 0
        self.index = 0

    def get_active(self):
        return False

    def update(self, FPS):
        self.tick += 1 / FPS
        if self.tick >= self.sec:
            self.index += 1
            self.index %= len(self.images_orig)
            self.set_image(self.images_orig[self.index])
            self.tick = 0


class ProgressBar(AnimationWidgets):
    def __init__(self, bar_top, bar_back, coord, from_color=(255, 255, 255), to_color=(255, 255, 255), percentage=0):
        if type(bar_top) == str:
            bar_top = load_image(bar_top)
        if type(bar_back) == str:
            bar_back = load_image(bar_back)
        bar_back.blit(bar_top, (0, 0))
        self.top_bar = bar_top
        self.back_bar = bar_back
        self.percentage = percentage
        self.color_from = from_color
        self.color_to = to_color
        self.display = None

        image = bar_back
        super().__init__(image, coord, 1, True)

    def add_display(self, display):
        self.display = display

    def update(self, FPS):
        pass

    def get_color(self, progress=None):
        if progress is None:
            progress = self.percentage
        res_color = []
        for color_1, color_2 in zip(self.color_from, self.color_to):
            if progress > 0.5:
                color_1 = color_1 * (1 - (progress - 0.5) * 2)
            if progress < 0.5:
                color_2 = color_2 * (progress * 2)
            res_color.append(min(255, color_1 + color_2))
        return res_color

    def update_bar(self, percentage):
        image = self.back_bar.copy()
        if percentage > 1:
            percentage = 1
        self.percentage = percentage
        h = self.back_bar.get_height()
        w = self.back_bar.get_width() * self.percentage
        # print(w, self.back_bar.get_width())
        color = self.get_color()
        for x in range(int((w + 1))):
            pygame.draw.line(image, color, [x, 0], [x, h])
        image.blit(self.top_bar, (0, 0))
        self.set_image(image)
        if self.display is not None:
            self.display.update_text(f'{int(self.percentage * 100)}%', color=self.get_color())


class Text(Widget):
    def __init__(self, text, size, coord, color=(255, 255, 255)):
        text_image = create_text(text, size, color)
        super().__init__(text_image, coord)
        self.text, self.font_size, self.font_color = text, size, color

    def get_active(self):
        return False

    def update_text(self, text=None, size=None, color=None):
        text = str(self.text if text is None else text)
        size = self.font_size if size is None else size
        color = self.font_color if color is None else color
        font_type = pygame.font.Font(FONT_STYLE, size)
        text = font_type.render(text, True, color)
        self.set_image(text)


# тест программы
if __name__ == '__main__':
    def set_mouse_vizible(then):
        app = then.get_application()
        if then.get_pressed():
            app.set_mouse_normal()
        else:
            app.set_mouse_image(0)


    test_app = Application((530, 500))
    widget2 = Button(['name2.png', 'name.png'], (10, 10), set_mouse_vizible, is_zooming=True)
    widget1 = AnimationWidgets([load_image('1.png', (255, 255, 255)), load_image('2.png', (255, 255, 255)),
                                load_image('3.png', (255, 255, 255))], (-120, -10), 0.65)
    lu = Widget('lu.png', (10, 10))
    lb = Widget('lb.png', (10, -10))
    ru = Widget('ru.png', (-10, 10))
    rb = Widget('rb.png', (-10, -10))
    mouse = 'mouse1.png'
    test_app.load_mouse_image(mouse)
    test_app.set_mouse_image(0)
    test_app.add_widget(widget2)
    test_app.add_widget(widget1)
    test_app.add_widget(lu, 0)
    test_app.add_widget(lb, 0)
    test_app.add_widget(ru, 0)
    test_app.add_widget(rb, 0)
    test_app.run()