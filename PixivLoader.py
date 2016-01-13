import cPickle
import os
from urlparse import urljoin

import requests
from flask import Flask, send_from_directory, send_file
from lxml import etree

from account import account
from settings import *

app = Flask(__name__)


class Pixiv:
    cookies_filename = os.path.join(app.root_path, 'cookies.pkl')
    base_urls = {
        'following_illust': 'http://www.pixiv.net/bookmark_new_illust.php?p=%s',
        'login': 'https://www.secure.pixiv.net/login.php',
        'test_login': 'http://www.pixiv.net/stacc/?mode=unify',
        'home': 'http://www.pixiv.net/',
    }
    session = requests.Session()
    session.proxies = PROXIES
    session.headers = HEADERS
    session.verify = False
    is_login = False

    def __init__(self):
        try:
            self.session.cookies = cPickle.load(open(self.cookies_filename, 'rb'))
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
        if response.url == u'http://www.pixiv.net/':
            self.is_login = True
            cPickle.dump(self.session.cookies, open(self.cookies_filename, 'wb'))

    def get(self, url, **kwargs):
        return self.session.get(url=url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.session.post(url=url, data=data, **kwargs)

    def get_following(self, page_number):
        response = self.get(self.base_urls['following_illust'] % page_number)
        result = list(self.parse_list(response))
        return result

    def parse_list(self, response):
        tree = etree.HTML(response.text)
        illusts = tree.xpath('//li[@class="image-item "]')
        for illust in illusts:
            illust_url = illust.xpath('./a/@href')[0]
            # todo cache thumbnails
            # todo get author and title
            is_multi = 'multiple' in illust.xpath('./a[0]/@class')[0]
            if is_multi:
                illust_url = illust_url.replace('medium', 'manga')
            illust_response = self.get(urljoin(self.base_urls['home'], illust_url), headers={'Referer': response.url})
            if is_multi:
                yield self.parse_manga(illust_response)
            else:
                yield self.parse_illust(illust_response)

    def parse_illust(self, response):
        tree = etree.HTML(response.text)
        img_src = tree.xpath('//div[starts-with(@class,"_illust_modal")]/div[@class="wrapper"]/img/@data-src')[0]
        # todo download pic and return
        pass

    def parse_manga(self, response):
        tree = etree.HTML(response.text)
        pics = tree.xpath('//div[@class="item-container"]')
        for pic in pics:
            img_src = pic.xpath('./img/@data-src')[0]
        # todo download pic and return
        pass


pixiv = Pixiv()


@app.route('/get_following/<int:page_number>')
def get_following(page_number):
    return pixiv.get_following(page_number)


@app.route('/')
def index_page():
    return send_file(os.path.join(app.static_folder, "index.html"))


@app.route('/<path:path>')
def static_html(path):
    return send_from_directory(app.static_folder, path)


if __name__ == '__main__':
    pixiv.login()
    # app.debug = True
    app.run()
