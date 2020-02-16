from Buttons import *
from Map import *
import pygame
# Импортируем необходимые модули


# Получаем актуальные размеры экрана, и создаём приложение
# size_screen = (GetSystemMetrics(0), GetSystemMetrics(1))
size_screen = (1000, 800)
pygame.init()
screen = pygame.display.set_mode(size_screen)

clock = pygame.time.Clock()

application = Application(size_screen, (100, 100, 100), False)
text_widget = TextWidget(None, [0, 0])
application.add_widget(text_widget, 2)
push_off = check_image('Widget_image/Button/delet_off.png', color_key=-1)
push_active = check_image('Widget_image/Button/delet_active.png', color_key=-1)
push_on = check_image('Widget_image/Button/delet_on.png', color_key=-1)
push_button = Button([push_off, push_active, push_on], text_widget.delete_text, [0.25, 0], name='delete_button')
slider_button_image = Smooth([0, 0], [50, 50], 25).generate_smooth()
slider_button = Slider(slider_button_image, [-0.005, 0.3], 0, 1, 300, color_slider=(200, 200, 50))
api_server = "http://static-maps.yandex.ru/1.x/"
print('generate')
params = {
    "ll": '0.0,0.0',
    'spn': "10.0,10.0",
    "l": "sat,skl",
    "z": "5",
    "size": "400,400"
}

map = Map((4000, 4000))
application.add_widget(map, 0)
# x
# min 0
# max 8230
# y
# min 0
# max 7905 
for y in range(-10, 11):
    for x in range(-10, 11):
        params["ll"] = generate_coord(x, y)
        params['spn'] = get_spn(y)
        map.add_chunk(requests.get(api_server, params=params), ((x + 10) * 10, (y + 10) * 10))
map.generate_image()
application.add_widget(map, 0)
create = False
if create:
    name_image = ['_off.png', '_on.png', '_active.png']
    c = [[180] * 3, [100, 100, 255], [230] * 3]
    for i in range(3):
        image = Smooth([0, 0], (200, 50), 25, c[i]).generate_smooth()
        image.blit(TextBox(30, '', color=(10, 10, 10)).get_image(), [42, 7])
        pygame.image.save(image, f'map{name_image[i]}')
sat_radio_button = RadioButton(['Widget_image/Button/sat_off.png', 'Widget_image/Button/sat_active.png',
                                'Widget_image/Button/sat_on.png'], None, (0.10, 0.94), 'sat')
map_radio_button = RadioButton(['Widget_image/Button/map_off.png', 'Widget_image/Button/map_active.png',
                                'Widget_image/Button/map_on.png'], None, (0.01, 0.94), 'map')
sat_skl_radio_button = RadioButton(['Widget_image/Button/sat_skl_off.png', 'Widget_image/Button/sat_skl_active.png',
                                    'Widget_image/Button/sat_skl_on.png'], None, (0.19, 0.94), 'sat_skl')
radio_list = RadioButtons([sat_radio_button, map_radio_button, sat_skl_radio_button])
sat_skl_radio_button.s_p()
application.add_widget(sat_radio_button, 2)
application.add_widget(map_radio_button, 2)
application.add_widget(sat_skl_radio_button, 2)
application.add_widget(slider_button, 2)
application.add_widget(push_button, 3)
application.run()
