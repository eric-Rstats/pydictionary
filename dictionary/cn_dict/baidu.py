# -*-coding: utf-8-*-
# Author : Christopher Lee
# License: Apache License
# File   : baidu.py
# Date   : 2017-04-14 14-10
# Version: 0.0.1
# Description: description of this file.

import datetime
import os

from lxml.html import fromstring
from ..common.storage import SQLiteStorage, NullStorage
from ..common.downloader import Downloader

__version__ = '0.0.1'
__author__ = 'Chris'

_dict_directory = os.path.abspath(os.path.dirname(__file__))


class BaiduChineseWordPageParser(object):
    def __init__(self, page_content):
        self._tree = fromstring(page_content)

    @property
    def pronunciation(self):
        try:
            p = (self._tree.xpath("//div[@id='pinyin']/h2/span/b/text()")[0]).strip()
            return p.replace('[', '').replace(']', '')
        except:
            return ''

    @property
    def paraphrase(self):
        try:
            return ''.join(x.strip() for x in self._tree.xpath("//div[@id='basicmean-wrapper']/div[1]/text()"))
        except:
            return ''

    @property
    def synonyms(self):
        try:
            return ' '.join(x.strip() for x in self._tree.xpath("//div[@id='synonym']//a/text()"))
        except:
            return ''

    @property
    def antonyms(self):
        try:
            return ' '.join(x.strip() for x in self._tree.xpath("//div[@id='antonym']//a/text()"))
        except:
            return ''

    @property
    def translation(self):
        try:
            return ''.join(x.strip() for x in self._tree.xpath("//div[@id='fanyi-wrapper']/div[1]//text()"))
        except:
            return ''


class BaiduChineseWordDictionary(object):
    """
    Website: `http://hanyu.baidu.com/`.
    """
    host = 'hanyu.baidu.com'
    timeout = 48
    parser = BaiduChineseWordPageParser

    def __init__(self, cache_database=None, enable_cache=True):
        """
        Use sqlite as it's backend database to store details of words.
        """
        if enable_cache is True:
            self._storage = SQLiteStorage(cache_database or os.path.join(_dict_directory, 'cache.db'))
        else:
            self._storage = NullStorage(cache_database)

        self._downloader = Downloader(self.host)
        self._prepare_cache()

    def query(self, word, check_cache=True, proxy=None):
        """
        Query a word from Baidu Hanyu website.

        :param word: `str` keyword to be queried.
        :param proxy:
                1. http proxy: `http://user:password@host:port`
                1. socks5 proxy: `socks://user:password@host:port`
            Note: run `pip3 install -U requests[socks]` before using socks proxy.
        :param check_cache: check local database before sending request to BaiduHanyu
        :return: details of this word.
        """
        assert isinstance(word, str)
        assert len(word) >= 2, RuntimeError('Expected a word, not a character: {}'.format(word))

        word = word.strip()

        if check_cache is True:
            cache = self.from_database(word)
            if cache is not None:
                return cache

        r = self._downloader.get(self.make_url(word), proxy=proxy, timeout=self.timeout)
        details = self._parse_page(word, r)

        if details:
            self.into_database(details)

        return details

    def from_database(self, word):
        result = self._storage.query('SELECT * FROM "baidu_chinese" WHERE word = ?',
                                     args=(word,))
        if result:
            result.pop('id')

        return result

    def into_database(self, details):
        columns = list(details.keys())
        sql = '''REPLACE INTO "baidu_chinese" ({}) VALUES ({})'''.format(', '.join(columns),
                                                                         ', '.join('?' for _ in range(len(columns))))
        args = [details.get(k) for k in columns]
        self._storage.execute(sql, args)

    def make_url(self, word):
        return 'http://{}/s?wd={}'.format(self.host, word)

    def _parse_page(self, word, response):
        try:
            parser = self.parser(response.content)

            return {
                'word': word,
                'pronunciation': parser.pronunciation,
                'paraphrase': parser.paraphrase,
                'synonyms': parser.synonyms,
                'antonyms': parser.antonyms,
                'translation': parser.translation,
                'url': response.url,
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as err:
            print('{}: {}'.format(word, err))
            return None

    def _prepare_cache(self):
        self._storage.execute('''CREATE TABLE IF NOT EXISTS "baidu_chinese" (
                             "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                             "word" TEXT NOT NULL,
                             "synonyms" TEXT,
                             "antonyms" TEXT,
                             "pronunciation" TEXT,
                             "paraphrase" TEXT,
                             "translation" TEXT,
                             "url" TEXT,
                             "timestamp" TEXT
                        );''')
