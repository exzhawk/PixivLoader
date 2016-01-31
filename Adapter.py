# -*- encoding: utf-8 -*-
# Author: Epix
import requests
from requests.adapters import HTTPAdapter, DEFAULT_POOLSIZE, DEFAULT_POOLBLOCK, DEFAULT_RETRIES

from settings import *


class RetryProxyAdapter(HTTPAdapter):
    def __init__(self, pool_connections=DEFAULT_POOLSIZE, pool_maxsize=DEFAULT_POOLSIZE, max_retries=DEFAULT_RETRIES,
                 pool_block=DEFAULT_POOLBLOCK, timeout=None, proxies=None):
        super().__init__(pool_connections, pool_maxsize, max_retries, pool_block)
        if proxies is None:
            proxies = {}
        self.proxies = proxies
        self.timeout = timeout
        self.max_retries.status_forcelist = (502,)

    def cert_verify(self, conn, url, verify, cert):
        pass

    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        return super(RetryProxyAdapter, self).send(request, stream, self.timeout, verify, cert, proxies=self.proxies)


if __name__ == '__main__':
    session = requests.Session()
    adapter = RetryProxyAdapter(max_retries=5, timeout=0.1, proxies=PROXIES)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.get('http://exz.me')
