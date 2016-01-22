# -*- encoding: utf-8 -*-
# Author: Epix
import os
import pickle
from urllib.parse import quote, urljoin

from lxml import etree
from requests_futures.sessions import FuturesSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Illust import *
from account import account
from settings import PROXIES, HEADERS, CACHE_DIR


class Pixiv:
    cookies_filename = os.path.join(os.path.dirname(__file__), 'cookies.pkl')
    base_urls = {
        'following_illust': 'http://www.pixiv.net/bookmark_new_illust.php?p=%s',
        'login': 'https://www.secure.pixiv.net/login.php',
        'test_login': 'http://www.pixiv.net/stacc/?mode=unify',
        'home': 'http://www.pixiv.net/',
    }
    engine = create_engine('sqlite:///data.db')
    db_session = sessionmaker()
    db_session.configure(bind=engine)
    # session = requests.Session()
    session = FuturesSession(max_workers=10)
    session.proxies = PROXIES
    session.headers = HEADERS
    session.verify = False
    is_login = False

    def __init__(self):
        try:
            self.session.cookies = pickle.load(open(self.cookies_filename, 'rb'))
        except IOError:
            pass

    def login(self):
        self.test_login()
        if self.is_login is False:
            self.do_login()
        print(self.is_login)

    def test_login(self):
        response = self.get(url=self.base_urls['test_login'], allow_redirects=False)
        if response.status_code == 200:
            self.is_login = True

    def do_login(self):
        account_extra = ('mode', 'login'), ('skip', '1')
        response = self.post(url=self.base_urls['login'], data=dict(account_extra, **account))
        if response.url == 'http://www.pixiv.net/':
            self.is_login = True
            pickle.dump(self.session.cookies, open(self.cookies_filename, 'wb'))

    def get(self, url, **kwargs):
        return self.session.get(url=url, **kwargs).result()

    def post(self, url, data=None, **kwargs):
        return self.session.post(url=url, data=data, **kwargs).result()

    def get_following(self, page_number):
        response = self.get(self.base_urls['following_illust'] % page_number)
        result = list(self.parse_list(response))
        return result

    def cache_pic(self, url, referer):
        file_name = quote(url, safe='')
        file_path = os.path.join(CACHE_DIR, file_name)
        if os.path.isfile(file_path):
            pass
        else:
            self.session.get(url, headers={'Referer': referer}, background_callback=self.save_pic)

    def save_pic(self, session, response):
        url = response.url
        file_name = quote(url, safe='')
        file_path = os.path.join(CACHE_DIR, file_name)
        with open(file_path, 'wb') as f:
            f.write(response.content)

    def parse_list(self, response):
        tree = etree.HTML(response.text)
        illusts = tree.xpath('//li[@class="image-item "]')
        for illust in illusts:
            illust_url = illust.xpath('./a/@href')[0]
            id = int(illust_url.split('=')[-1])
            query = self.db_session.query(Illust).all
            illust_author = illust.xpath('./a[@class="user ui-profile-popup"]')[0]
            illust_author_name = illust_author.xpath('./@data-user_name')[0]
            illust_author_id = illust_author.xpath('./@data-user_id')[0]
            illust_title = illust.xpath('./a/h1[@class="title"]/text()')[0]
            illust_thumbnail_url = illust.xpath('./a/div[@class="_layout-thumbnail"]/img[@class="_thumbnail"]/@src')[0]
            self.cache_pic(illust_thumbnail_url, response.url)
            is_multi = 'multiple' in illust.xpath('./a[1]/@class')[0]
            if is_multi:
                illust_url = illust_url.replace('medium', 'manga')
            illust_response = self.get(urljoin(self.base_urls['home'], illust_url), headers={'Referer': response.url})
            meta = {'url': illust_url,
                    'title': illust_title,
                    'author_name': illust_author_name,
                    'author_id': illust_author_id,
                    'thumbnail': illust_thumbnail_url,
                    'is_multi': is_multi}
            if is_multi:
                yield self.parse_manga(illust_response, meta)
            else:
                yield self.parse_illust(illust_response, meta)

    def parse_illust(self, response, meta):
        d = dict(meta)
        tree = etree.HTML(response.text)
        img_src = tree.xpath('//div[starts-with(@class,"_illust_modal")]/div[@class="wrapper"]/img/@data-src')[0]
        self.cache_pic(img_src, response.url)
        d['img'] = [img_src]
        return d

    def parse_manga(self, response, meta):
        d = dict(meta)
        d['img'] = []
        tree = etree.HTML(response.text)
        pics = tree.xpath('//div[@class="item-container"]')
        for pic in pics:
            img_src = pic.xpath('./img/@data-src')[0]
            self.cache_pic(img_src, response.url)
            d['img'].append(img_src)
        return d
