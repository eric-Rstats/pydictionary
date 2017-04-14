# -*-coding: utf-8-*-
# Author : Christopher Lee
# License: Apache License
# File   : downloader.py
# Date   : 2017-04-14 14-03
# Version: 0.0.1
# Description: page downloader.

import requests

__version__ = '0.0.1'
__author__ = 'Chris'


class Downloader(object):
    """
    Request downloader
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'hanyu.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/57.0.2987.133 Safari/537.36'
    }

    def __init__(self, host):
        super().__init__()
        self._headers = self.headers.copy()
        self._headers['Host'] = host

    def get(self, url, params=None, proxy=None, **kwargs):
        try:
            if proxy:
                proxies = {
                    'http': proxy,
                    'https': proxy
                }
            else:
                proxies = None

            response = requests.get(url, params, proxies=proxies, headers=self._headers, **kwargs)
            if response.status_code == 200:
                return response
            else:
                return None
        except Exception as err:
            print('{}: {}'.format(url, err))
            return None

    def post(self, url, data=None, proxy=None, **kwargs):
        try:
            if proxy:
                proxies = {
                    'http': proxy,
                    'https': proxy
                }
            else:
                proxies = None

            response = requests.get(url, data=data, proxies=proxies, headers=self._headers, **kwargs)
            if response.status_code == 200:
                return response
            else:
                return b''
        except Exception as err:
            print('{}: {}'.format(url, err))
            return None
