# -*- encoding: utf-8 -*-
# Author: Epix
import os
from urllib.parse import quote, urljoin

from lxml import etree
from requests_futures.sessions import FuturesSession

from Cache import *
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
    # session = requests.Session()
    session = FuturesSession(max_workers=10)
    session.proxies = PROXIES
    session.headers = HEADERS
    session.verify = False
    is_login = False
    cache_db = CacheDb('cache_db.pkl')

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
        r = self.session.get(url=url, **kwargs).result()
        if r.status_code in (200, 301, 302, 500):
            return r
        else:
            return self.get(url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.session.post(url=url, data=data, **kwargs).result()

    def get_following(self, page_number):
        response = self.get(self.base_urls['following_illust'] % page_number)
        result = list(self.parse_list(response))
        return result

    def parse_list(self, response):
        tree = etree.HTML(response.text)
        illusts = tree.xpath('//li[@class="image-item "]')
        for illust in illusts:
            illust_url = illust.xpath('./a/@href')[0]
            illust_id = int(illust_url.split('=')[-1])
            cache_data = self.cache_db.get(illust_id)
            if cache_data:
                yield cache_data
            else:
                illust_author = illust.xpath('./a[@class="user ui-profile-popup"]')[0]
                illust_author_name = illust_author.xpath('./@data-user_name')[0]
                illust_author_id = illust_author.xpath('./@data-user_id')[0]
                illust_title = illust.xpath('./a/h1[@class="title"]/text()')[0]
                illust_thumbnail_url = illust.xpath('./a/div/img[@class="_thumbnail"]/@src')[0]
                self.cache_pic(illust_thumbnail_url, response.url)
                class_names = illust.xpath('./a[1]/@class')[0]
                is_multi = 'multiple' in class_names
                is_ugoku = 'ugoku-illust' in class_names
                illust_special = ''
                if is_multi:
                    illust_url = illust_url.replace('medium', 'manga')
                if is_multi:
                    illust_special = 'multi'
                elif is_ugoku:
                    illust_special = 'ugoku'
                illust_response = self.get(urljoin(self.base_urls['home'], illust_url),
                                           headers={'Referer': response.url})
                meta = {'url': illust_url,
                        'title': illust_title,
                        'author_name': illust_author_name,
                        'author_id': illust_author_id,
                        'thumbnail': self.quote_url(illust_thumbnail_url),
                        'special': illust_special}
                if is_multi:
                    illust_data = self.parse_manga(illust_response, meta)
                elif is_ugoku:
                    illust_data = self.parse_ugoku(illust_response, meta)
                else:
                    illust_data = self.parse_illust(illust_response, meta)
                self.cache_db.set(illust_id, illust_data)
                yield illust_data

    def parse_illust(self, response, meta):
        return self.parse_by_xpath(response, meta, '//div[starts-with(@class,"_illust_modal")]/div[@class="wrapper"]')

    def parse_manga(self, response, meta):
        return self.parse_by_xpath(response, meta, '//div[@class="item-container"]')

    def parse_ugoku(self, response, meta):
        d = dict(meta)
        d['img'] = []
        d['img'].append('')
        return d

    def parse_by_xpath(self, response, meta, xpath_str):
        d = dict(meta)
        d['img'] = []
        tree = etree.HTML(response.text)
        pics = tree.xpath(xpath_str)
        for pic in pics:
            img_src = pic.xpath('./img/@data-src')[0]
            self.cache_pic(img_src, response.url)
            d['img'].append(self.quote_url(img_src))
        return d

    def cache_pic(self, url, referer):
        file_name = self.quote_url(url)
        file_path = os.path.join(CACHE_DIR, file_name)
        if os.path.isfile(file_path):
            pass
        else:
            self.session.get(url, headers={'Referer': referer}, background_callback=self.save_pic)

    def quote_url(self, url):
        return quote(url, safe='')

    def save_pic(self, session, response):
        if response.status_code in (200, 301, 302, 500):
            url = response.url
            file_name = self.quote_url(url)
            file_path = os.path.join(CACHE_DIR, file_name)
            with open(file_path, 'wb') as f:
                f.write(response.content)
        else:
            self.session.get(response.url, headers=response.request.headers, background_callback=self.save_pic)
