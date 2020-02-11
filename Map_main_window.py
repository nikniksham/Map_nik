from Widget import *
import pygame
from win32api import GetSystemMetrics
# Импортируем необходимые модули


# Получаем актуальные размеры экрана, и создаём приложение
size_screen = (GetSystemMetrics(0), GetSystemMetrics(1))
pygame.init()
screen = pygame.display.set_mode(size_screen, pygame.FULLSCREEN)

clock = pygame.time.Clock()


def update_screen():
    # Обнавление экрана
    pass


widgets = Widgets(screen)
text_widget = TextWidget(None, [0, 0])
widgets.add_widget(text_widget)
space = backspace = False
tick = 0
while True:
    tick += 1
    screen.fill((0, 0, 0))
    # Обработка клавиш и событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space = True
            if event.key == pygame.K_BACKSPACE:
                backspace = True
            if text_widget.get_active():
                text_widget.write_text(event, space, backspace)
            if event.key == pygame.K_ESCAPE:
                quit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space = False
            if event.key == pygame.K_BACKSPACE:
                backspace = False
    if text_widget.get_active() and tick >= 1:
        tick = 0
        text_widget.write_text(None, space, backspace)
    widgets.update()
    pygame.display.flip()
