from Widget import ThreadApp
import requests


class WebLoad(ThreadApp):
    def __init__(self, url: str, params: dict):
        """Делает запрос и возвращает результат request
        url - адресс с которого надо загрузить
        params - параметры для запроса"""
        self.url = url
        self.params = params

    def run(self):
        """Запуск потока"""
        global thread_break
        # Скачиваем файл
        self.download_file(self.url)
        # Статус завершили работать
        self.status = False
        thread_break = True

    def get_res(self):
        res = self.res
        self.res = None
        return res

    def download_file(self, url):
        """Скачиваем файл"""
        self.res = requests.get(self.url, params=self.params)


class LoadMap(ThreadApp):
    def __init__(self, map_widget):
        pass
