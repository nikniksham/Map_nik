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
slider_button_image = Smooth([0, 0], [50, 50], 25).generate_smooth()
slider_button = Slider(slider_button_image, [400, 400], 0, 1, 100, color_slider=(200, 200, 50))
pygame.image.save(slider_button_image, 'test.png')
application.add_widget(slider_button, 2)
application.add_widget(push_button, 2)
application.run()
