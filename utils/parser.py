import requests
from bs4 import BeautifulSoup as BS


class Parser:
    def __init__(self):
        pass

    def get_vk(self, url: str) -> dict:
        with requests.session() as sess:
            page = sess.get(url)
            soup = BS(page)
            print(soup)