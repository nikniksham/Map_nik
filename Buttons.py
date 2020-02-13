from Widget import *


class Button(Widget):
    def __init__(self, images, action, coord, toggle=False):
        """Загрузка картинок, действие, координаты, тип - push, toggle"""
        self.images = []
        for image in images:
            self.images.append(check_image(image, 'image_button'))
        self.action = action
        self.pressed = False
        self.toggle = toggle
        super().__init__(self.images[0], coord)
        self.set_image(check_image(self.images[0]))

    def get_active(self):
        return self.active or self.pressed

    def get_pressed(self):
        return self.pressed

    def set_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if not self.toggle:
                if self.pressed:
                    self.pressed = not self.pressed
                else:
                    self.pressed = event.button == 1 and self.rect.collidepoint(event.pos)
            else:
                if self.pressed and self.rect.collidepoint(event.pos):
                    self.pressed = False
                else:
                    self.pressed = event.button == 1

    def get_surface(self):
        if not self.pressed:
            if self.active:
                return self.images[1]
            else:
                return self.images[0]
        else:
            return self.images[2]

    def update(self, event):
        """Обновление стандартной кнопки"""
        if event.type == pygame.MOUSEBUTTONUP:
            self.set_pressed(event)
            if self.get_pressed():
                self.set_image(self.images[2])
                if self.action is not None:
                    self.action(self)


class TextWidget(Button):
    def __init__(self, image, coord):
        if image is None:
            self.image = Smooth((0, 0), size_screen.get_size(0.3, 0.05), int(size_screen.get_size(0.3, 0.015)[1]),
                                (200, 200, 200)).generate_smooth()
        else:
            self.image = check_image(image, 'image_text_widget')
        self.action = self.write_text
        self.pressed = False
        self.tick = 0
        self.len_text = 0
        self.text = ''
        super().__init__([self.image] * 2, self.write_text, coord)

    def get_surface(self):
        return self.image

    def set_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and event.button == 1:
                self.pressed = not self.pressed
            else:
                self.pressed = event.button == 1 and self.rect.collidepoint(event.pos)

    def write_text(self, keys):
        """Функция написания текста в виджете TextWidget"""
        # print(keys)
        # Получение имени клавиши, если в программе выбран язык - английский, если выбран русский, то
        # подключается словарь "мазахиста"
        for key in keys:
            key_name = pygame.key.name(key)
            if key_name == 'return':
                self.set_active(False)
                return
            if key_name in good_symbols and self.len_text <= 16000:
                # Проверка раскладки
                if get_lang() == 'eng':
                    self.text += key_name
                if get_lang() == 'ru':
                    if key_name in list(rus_text.keys()):
                        self.text += rus_text[key_name]
                    else:
                        self.text += key_name
            if key_name == 'space' and self.len_text <= 16000:
                self.text += ' '
            if key_name == 'backspace':
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
        event = args[0]
        self.tick += 1
        if self.tick >= 7:
            if event.type == 'buttons' and self.get_pressed() or self.active:
                self.tick = 0
                self.write_text(self.app.pressed_key)
            size_screen.set_size(self.app.size_screen[0], self.app.size_screen[1])
            image = Smooth((0, 0), size_screen.get_size(0.3, 0.05), int(size_screen.get_size(0.3, 0.015)[1]),
                           (200, 200, 200)).generate_smooth()
            text = TextBox(size_screen.get_size(0.3, 0.035)[1], self.get_normal_text()).get_image()
            self.len_text = text.get_width()
            image.blit(text, [10, 0], ((text.get_width() - size_screen.get_size(0.24, 0)[0], 0),
                                       size_screen.get_size(0.24, 0.05)))
            self.set_image(image)
        self.set_pressed(event)