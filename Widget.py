import pygame
import os
from pygame.draw import *
from win32api import GetSystemMetrics
from ctypes import *

user32 = windll.user32

# Определяем язык ввода
hwnd = user32.GetForegroundWindow()
threadID = user32.GetWindowThreadProcessId(hwnd, None)
StartLang = user32.GetKeyboardLayout(threadID)
# print(StartLang)
# 68748313
# 67699721


def get_lang():
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
        self.language = 'eng'
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
                if self.language == 'eng':
                    self.text += key_name
                if self.language == 'rus':
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
