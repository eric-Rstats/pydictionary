# -*-coding: utf-8-*-
# Author : Christopher Lee
# License: Apache License
# File   : tests.py
# Date   : 2017-04-14 16-08
# Version: 0.0.1
# Description: description of this file.

from pprint import pprint
from concurrent.futures import ThreadPoolExecutor

from dictionary import BaiduChineseWordDictionary


def test_query_words(words):
    d = BaiduChineseWordDictionary(cache_database='./dict.db', enable_cache=True)

    for w in words:
        pprint(d.query(w))
        print()


d = BaiduChineseWordDictionary(cache_database='./dict.db')


def query(word):
    pprint(d.query(word))


def threading_pool_test():
    ws = [x.strip() for x in open('words.txt') if x.strip()][:1000]
    ThreadPoolExecutor(15).map(query, ws)


if __name__ == '__main__':
    # wds = '麻木不仁 漠不关心 不知甘苦 不省人事 麻痹不仁 多管闲事 不知痛痒 无动于衷 ' \
    #       '黎明 早晨 凌晨 天后 破晓 平旦 清晨 平明 拂晓 ' \
    #       '黑白分明 泾渭分明 一清二白 大是大非 判若黑白 白璧青蝇 爱憎分明 一清二楚 判若鸿沟'.split()
    # test_query_words(wds)
    threading_pool_test()
