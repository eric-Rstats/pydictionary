# -*-coding: utf-8-*-
# Author : Christopher Lee
# License: Apache License
# File   : tests.py
# Date   : 2017-04-14 16-08
# Version: 0.0.1
# Description: description of this file.

from pprint import pprint

from dictionary import BaiduChineseWordDictionary


def test_query_words(words):
    d = BaiduChineseWordDictionary(cache_database='./dict.db', enable_cache=True)

    for w in words:
        pprint(d.query(w))
        print()


if __name__ == '__main__':
    wds = '麻木不仁 漠不关心 不知甘苦 不省人事 麻痹不仁 多管闲事 不知痛痒 无动于衷'.split()
    test_query_words(wds)
