# -*- encoding: utf-8 -*-
# Author: Epix
PROXY = ('127.0.0.1', '8089')
PROXIES = {
    'http': 'http://%s:%s' % PROXY,
    'https': 'http://%s:%s' % PROXY,
}
PROXY_HOST, PROXY_PORT = PROXY
CACHE_DIR = 'H:\TEMP\p_cache'
