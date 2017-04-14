# 汉语词典查询接口
计划是在该汉语**词典**（Not **字典**）包中封装多种平台提供的词语查询功能，并提供统一格式的返回结果。目前仅实现了**[百度汉语](http://hanyu.baidu.com/)**提供的词语查询功能。

# 功能
1. 提供非常简单的查询接口，用于获取词语的释义、同义词、反义词等；
1. 默认提供数据库缓存功能，内部使用 `sqlite` 进行缓存，加速后期查询；
1. 可自由选择从缓存获取词语详情或强制从平台查询最新的结果；
1. 提供代理请求功能（方便大规模获取词语释义的情况），支持 `http/https/socks5` 代理。

# 注意
1. 如需 `socks5` 代理支持，需要安装 `requests` 增强版：`pip3 install -U requests[socks]`。

# 安装
1. 下载该 `package` 的源码；
1. 运行 `Python3 setup.py install` 进行安装（仅支持 Python 3.x）。

# 示例
1. 实例化一个字典对象：

```python
from dictionary import BaiduChineseWordDictionary

# 默认启用数据库缓存功能，默认数据库位于包内部
bd_dic = BaiduChineseWordDictionary()

# 禁用缓存功能
bd_dic = BaiduChineseWordDictionary(enable_cache=False)

# 使用自定义的缓存数据库
bd_dic = BaiduChineseWordDictionary(cache_database='/path/to/database.db')
```

2. 查询词语

```python
# 默认查询方式
bd_dic.query("受宠若惊")

# 不使用缓存查询
bd_dic.query("受宠若惊", check_cache=False)

# 使用 http 代理
bd_dic.query('受宠若惊', proxy="http://user:password@host:port")

# 使用 socks5 代理（需要安装 `requests[socks]`）
bd_dic.query('受宠若惊', proxy='socks5://user:password@host:port')
```