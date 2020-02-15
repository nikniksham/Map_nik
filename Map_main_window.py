from Buttons import *
import pygame
# Импортируем необходимые модули


# Получаем актуальные размеры экрана, и создаём приложение
# size_screen = (GetSystemMetrics(0), GetSystemMetrics(1))
size_screen = (1000, 800)
pygame.init()
screen = pygame.display.set_mode(size_screen)

clock = pygame.time.Clock()

application = Application(size_screen, (200, 0, 0), False)
text_widget = TextWidget(None, [0, 0])
application.add_widget(text_widget, 2)
push_off = check_image('Widget_image/Button/delet_off.png', color_key=-1)
push_active = check_image('Widget_image/Button/delet_active.png', color_key=-1)
push_on = check_image('Widget_image/Button/delet_on.png', color_key=-1)
push_button = Button([push_off, push_active, push_on], text_widget.delete_text, [0.25, 0], name='delete_button')
slider_button_image = Smooth([0, 0], [50, 50], 25).generate_smooth()
slider_button = Slider(slider_button_image, [400, 200], 0, 1, 300, color_slider=(200, 200, 50))
pygame.image.save(slider_button_image, 'test.png')
application.add_widget(slider_button, 2)
application.add_widget(push_button, 3)
application.run()
