# -*- encoding: utf-8 -*-
# Author: Epix
import os
from urllib.parse import quote

import requests
from pixivpy3 import PixivAPI, PixivError
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from Adapter import RetryProxyAdapter
from Cache import *
from account import account
from settings import *


class PixivRetryProxyAPI(PixivAPI):
    session = requests.Session()
    adapter = RetryProxyAdapter(max_retries=5, timeout=5, proxies=PROXIES)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    def requests_call(self, method, url, headers=None, params=None, data=None):
        req_header = {
            'Referer': 'http://spapi.pixiv.net/',
            'User-Agent': 'PixivIOSApp/5.8.3',
        }
        req_header.update(headers)

        try:
            if method == 'GET':
                return self.session.get(url, params=params, headers=req_header)
            elif method == 'POST':
                return self.session.post(url, params=params, data=data, headers=req_header)
            elif method == 'DELETE':
                return self.session.delete(url, params=params, data=data, headers=req_header)
        except Exception as e:
            raise PixivError('requests %s %s error: %s' % (method, url, e))

        raise PixivError('Unknown method: %s' % method)


class Pixiv:
    cache_db = CacheDb('cache_db.pkl')

    token_filename = os.path.join(os.path.dirname(__file__), 'token.pkl')
    api_cache_filename = os.path.join(os.path.dirname(__file__), 'api_cache.pkl')
    api_cache = CacheDb(api_cache_filename)
    pixiv_api = PixivRetryProxyAPI()
    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    http_client = AsyncHTTPClient()
    referer_base_url = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s'

    def __init__(self):
        try:
            self.pixiv_api.refresh_token = pickle.load(open(self.token_filename, 'rb'))
            self.pixiv_api.auth()
        except:
            self.pixiv_api.login(account['pixiv_id'], account['pass'])
            pickle.dump(self.pixiv_api.refresh_token, open(self.token_filename, 'wb'))

    def get_following(self, page_number):
        following_works_json = self.pixiv_api.me_following_works(page=page_number)
        following_works_ids = [i['id'] for i in following_works_json['response']]
        result_json = []
        for following_works_id in following_works_ids:
            cached_data = self.cache_db.get(following_works_id)
            if cached_data:
                result_json.append(cached_data)
            else:
                r = self.pixiv_api.works(following_works_id)
                cache_data = r['response'][0]
                self.cache_db.set(following_works_id, cache_data)
                result_json.append(cache_data)
        return result_json

    @gen.coroutine
    def cache_pic(self, json_list):
        for illust in json_list:
            illust_id = illust['id']
            referer_url = self.referer_base_url % illust_id
            illust_thumbnail_url = illust['image_urls']['small']
            self.fetch_pic(illust_thumbnail_url, referer_url)
            if illust['is_manga']:
                for illust_p in illust['metadata']['pages']:
                    illust_url = illust_p['image_urls']['large']
                    self.fetch_pic(illust_url, referer_url)
            elif illust['type'] == 'ugoira':
                illust_url = tuple(illust['metadata']['zip_urls'].values())[0]
                self.fetch_pic(illust_url, referer_url)
            else:
                illust_url = illust['image_urls']['large']
                self.fetch_pic(illust_url, referer_url)

    @gen.coroutine
    def fetch_pic(self, url, referer):
        if not os.path.isfile(self.url2path(url)):
            self.http_client.fetch(url, self.save_pic, proxy_host=PROXY_HOST, proxy_port=int(PROXY_PORT),
                                   headers={'referer': referer},
                                   user_agent='Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML,'
                                              ' like Gecko) Chrome/48.0.2564.97 Safari/537.36')

    @gen.coroutine
    def save_pic(self, response):
        if response.code in (502,) or response.body is None:
            self.fetch_pic(response.effective_url, response.request.headers['referer'])
        else:
            url = response.effective_url
            file_path = self.url2path(url)
            with open(file_path, 'wb') as f:
                f.write(response.body)

    @staticmethod
    def quote_url(url):
        return quote(url, safe='')

    def url2path(self, url):
        file_name = self.quote_url(url)
        file_path = os.path.join(CACHE_DIR, file_name)
        return file_path
