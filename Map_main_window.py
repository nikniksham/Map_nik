from Buttons import *
import pygame
# Импортируем необходимые модули


# Получаем актуальные размеры экрана, и создаём приложение
# size_screen = (GetSystemMetrics(0), GetSystemMetrics(1))
size_screen = (800, 600)
pygame.init()
screen = pygame.display.set_mode(size_screen, pygame.RESIZABLE)

clock = pygame.time.Clock()

application = Application(size_screen, (0, 0, 0), False)
text_widget = TextWidget(None, [0, 0])
application.add_widget(text_widget, 2)
push_off = check_image('Widget_image/Button/delet_off.png')
push_active = check_image('Widget_image/Button/delet_active.png')
push_on = check_image('Widget_image/Button/delet_on.png')
push_button = Button([push_off, push_active, push_on], text_widget.delete_text, [200, 200])
application.add_widget(push_button, 2)
application.run()
