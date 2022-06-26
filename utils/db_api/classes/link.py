import base64
import hashlib
import re
from dataclasses import dataclass
from datetime import datetime

import requests
from bs4 import BeautifulSoup as BS

from aiogram.utils.markdown import hlink


@dataclass
class Link:
    id: int
    date: datetime
    hash: int
    link: str

    def __post_init__(self):
        self.hash = int(self.hash)
        self.link = self.link[:-1] if self.link[-1] == '/' else self.link

        self.vk_public_count = int(str(self.hash)[0]) if int(str(self.hash)[0]) < 7 else 0
        self.telegram_count = int(str(self.hash)[1]) if int(str(self.hash)[1]) < 7 else 0
        self.darknet_count = int(str(self.hash)[2]) if int(str(self.hash)[2]) < 7 else 0
        self.self_count = int(str(self.hash)[3]) if int(str(self.hash)[3]) < 6 else 0
        self.total_count = sum((self.vk_public_count, self.telegram_count, self.darknet_count, self.self_count))

        self.vk_id = self.hash // 10000
        self.new_hash = self.hash ** 2 // 1000000000000
        self.year = str(datetime.now().year)
        self.new_date = datetime.fromtimestamp(self.hash // 1000).strftime(f"{self.year}-%m-%d_%H-%M-")

        self.places = [
            ('Поиск по приватным телеграм каналам...', 'полминуты', (15, 30), self.vk_public_count),
            ('Поиск по закрытым пабликам ВК...', 'минута', (30, 60), self.telegram_count),
            ('Поиск по даркнет форуму...', 'полминуты', (15, 30), self.darknet_count),
            ('Поиск по архиву страницы...', '10 сек', (7, 10), self.self_count),
        ]

        self.places = [
            ('Поиск по приватным телеграм каналам...', 'полминуты', (0, 0),
             self.vk_public_count),
            ('Поиск по закрытым пабликам ВК...', 'минута', (0, 0),
             self.telegram_count),
            ('Поиск по даркнет форуму...', 'полминуты', (0, 0),
             self.darknet_count),
            (
            'Поиск по архиву страницы...', '10 сек', (0, 0), self.self_count),
        ]


        if 'vk.com/' in self.link:
            self.user = self.get_vk()
        elif 'instagram.com/' in self.link:
            self.user = self.get_insta()
        elif 'tiktok.com/' in self.link:
            self.user = self.get_tiktok()
        else:
            raise WrongUrlError

        self.user_text = f"<b>{hlink(self.user['name'], self.link)}</b>\n{self.user['info']}\n"
        self.price_ratio = 49
        self.price = int(self.total_count * self.price_ratio)
        self.price_with_discount = int(self.total_count * self.price_ratio * 0.75)

    @property
    def text(self):
        if self.total_count:
            text = [
                self.user_text,
                f'Найдено <b>{self.total_count}</b> слитых интимных материалов'
            ]

            if self.telegram_count:
                text += ['\n<b>Приватные телеграм каналы</b>']
                for n in range(self.telegram_count):
                    is_photo = int(str(self.hash)[n]) % 3 != 0
                    emoji = "🖼" if is_photo else "📹"
                    file_type = "photo_" if is_photo else "video_"
                    format = ".jpg" if is_photo else ".mp4"
                    file = hlink(file_type + self.new_date + str(int(str(self.hash)[-2:]) + n) + format,
                                 "t.me/nudes_robot")
                    text += [f'    {emoji} {file}']

            if self.vk_public_count:
                text += ['\n<b>Закрытые паблики ВК</b>']
                for n in range(self.vk_public_count):
                    is_photo = int(str(self.hash)[::-1][n]) % 3 != 0
                    emoji = "🖼" if is_photo else "📹"
                    file_type = "photo" if is_photo else "video"
                    format = ".jpg" if is_photo else ".mp4"
                    file = hlink(file_type + "205485890_" + str(self.vk_id + n) + format,
                                 "t.me/nudes_robot")
                    text += [f'    {emoji} {file}']

            if self.darknet_count:
                text += ['\n<b>Даркнет форум</b>']
                for n in range(self.darknet_count):
                    is_photo = int(str(self.new_hash)[n]) % 3 != 0
                    emoji = "🖼" if is_photo else "📹"
                    format = ".jpeg" if is_photo else ".mov"
                    rand_string = hashlib.md5(
                        str(self.hash + n).encode('utf-8')).hexdigest()[:20]
                    file = hlink(rand_string + format,
                                 "t.me/nudes_robot")
                    text += [f'    {emoji} {file}']

            if self.self_count:
                text += ['\n<b>Архив страницы</b>']
                for n in range(self.self_count):
                    is_photo = int(str(self.new_hash)[::-1][n]) % 3 != 0
                    emoji = "🖼" if is_photo else "📹"
                    format = ".jpg" if is_photo else ".mp4"
                    rand_string = hashlib.md5(
                        str(self.hash * 10 + n).encode('utf-8')).hexdigest()[:10]
                    file = hlink(f"archive_{self.year}_" + rand_string + format,
                                 "t.me/nudes_robot")
                    text += [f'    {emoji} {file}']

            text += [
                f'\nЦена: <s>{self.price}₽</s>',
                'Скидка на первый заказ: <b>25%</b>',
                f'<b>Итоговая цена: {self.price_with_discount}₽</b>'
            ]

        else:
            text = ['<b>Не удалось найти никаких материалов</b>']

        return text

    def get_tiktok(self):
        with requests.session() as sess:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.216 YaBrowser/21.5.4.607 Yowser/2.5 Safari/537.36',
            }

            response = sess.get(self.link, headers=headers)
            if not response:
                raise WrongUrlError

            soup = BS(response.content, 'html.parser')
            image = sess.get(soup.select('.tiktok-avatar img')[0]['src'],
                             headers=headers).content
            numbers = list(map(lambda x: x.text, soup.select('strong')[1:]))
            info = ' | '.join(map(lambda x: " ".join(x), zip(numbers, (
            'Подписки', 'Подписчики', 'Лайки'))))

            user = {}
            user['name'] = self.link.split('/')[-1]
            user['info'] = info
            user['image'] = image
            return user

    def get_insta(self):
        with requests.session() as sess:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.216 YaBrowser/21.5.4.607 Yowser/2.5 Safari/537.36',
            }

            response = sess.get(
                'https://insta-stories.online/' + self.link.split('/')[-1],
                headers=headers)
            if not response:
                raise WrongUrlError

            soup = BS(response.content, 'html.parser')
            photo = re.findall(r"profile-pic\" src=\".+\" a", str(soup))[0][
                    41:-3]
            image = base64.b64decode(photo)
            numbers = list(map(lambda x: x.text,
                               soup.select('.user-info .info ul li span')))
            info = ' | '.join(map(lambda x: " ".join(x), zip(numbers, (
            'Публикаций', 'Подписчиков', 'Подписок'))))

            user = {}
            user['name'] = self.link.split('/')[-1]
            user['info'] = info
            user['image'] = image
            return user

    def get_vk(self):
        with requests.session() as sess:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.216 YaBrowser/21.5.4.607 Yowser/2.5 Safari/537.36'
            }

            data = {
                'id': self.link,
                'user': 'Найти'
            }

            response = sess.post('https://vk-photo.info/', headers=headers,
                                 data=data)
            if not response:
                raise WrongUrlError

            soup = BS(response.content, 'html.parser')
            image = sess.get(soup.select('.rounded-circle')[0]['src'],
                             headers=headers).content
            info = list(filter(lambda x: 'Дата' in x, map(lambda y: y.text,soup.select('.h5, h5'))))
            info = info[0].split(': ')[1] if info else ''

            user = {}
            user['name'] = soup.select('.profile')[0].text.split('\n')[0]
            user['info'] = info
            user['image'] = image
            return user


class WrongUrlError(Exception):
    pass