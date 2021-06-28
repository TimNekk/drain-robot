import re

import requests
from bs4 import BeautifulSoup as BS
import base64


class WrongUrlError(Exception):
    pass


def get_tiktok(url: str):
    with requests.session() as sess:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.216 YaBrowser/21.5.4.607 Yowser/2.5 Safari/537.36',
        }

        response = sess.get(url, headers=headers)
        if not response:
            raise WrongUrlError

        soup = BS(response.content, 'html.parser')
        image = sess.get(soup.select('.tiktok-avatar img')[0]['src'], headers=headers).content
        numbers = list(map(lambda x: x.text, soup.select('strong')[1:]))
        info = ' | '.join(map(lambda x: " ".join(x), zip(numbers, ('Подписки', 'Подписчики', 'Лайки'))))

        user = {}
        user['name'] = url.split('/')[-1]
        user['info'] = info
        user['image'] = image

        with open('image.png', 'wb') as f:
            f.write(image)
        return


# print(get_tiktok('https://www.tiktok.com/@tikd'))


def get_insta(url: str):
    with requests.session() as sess:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.216 YaBrowser/21.5.4.607 Yowser/2.5 Safari/537.36',
        }

        response = sess.get(
            'https://insta-stories.online/' + url.split('/')[-1], headers=headers)
        if not response:
            raise WrongUrlError

        soup = BS(response.content, 'html.parser')
        photo = re.findall(r"profile-pic\" src=\".+\" a", str(soup))[0][41:-3]
        image = base64.b64decode(photo)
        numbers = list(map(lambda x: x.text, soup.select('.user-info .info ul li span')))
        info = ' | '.join(map(lambda x: " ".join(x), zip(numbers, ('Публикаций', 'Подписчиков', 'Подписок'))))

        user = {}
        user['name'] = url.split('/')[-1]
        user['info'] = info
        user['image'] = image
        return user


def get_vk(url: str):
    with requests.session() as sess:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.216 YaBrowser/21.5.4.607 Yowser/2.5 Safari/537.36'
        }

        data = {
            'id': url,
            'user': 'Найти'
        }

        response = sess.post('https://vk-photo.info/', headers=headers,
                             data=data)
        if not response:
            raise WrongUrlError

        soup = BS(response.content, 'html.parser')
        image = sess.get(soup.select('.rounded-circle')[0]['src'], headers=headers).content

        user = {}
        user['name'] = soup.select('.profile')[0].text.split('\n')[0]
        user['info'] = list(filter(lambda x: 'Дата' in x, map(lambda y: y.text, soup.select('.h5, h5'))))[0].split(': ')[1]
        user['image'] = image
        return user