# -*- encoding: utf-8 -*-
# Author: Epix
PROXY = ('127.0.0.1', '8888')
PROXIES = {
    'http': 'http://%s:%s' % PROXY,
    'https': 'http://%s:%s' % PROXY,
}
PROXY_HOST, PROXY_PORT = PROXY
HEADERS = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
}
CACHE_DIR = 'H:\TEMP\p_cache'
