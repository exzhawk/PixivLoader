# PixivLoader

Just anther pixiv client with aggressive cache.

#Dependency

* Python 3
* Tornado 
* requests
* pixivpy3

##Usage

Create a file named "account.py" in the same directory of PixivLoader.py
And write you credential info in it in following format.

```python
account = {
    'pixiv_id': 'Your Pixiv Username',
    'pass': 'Your Pixiv Password',
}
```

Run PixivLoader.py

Open http://127.0.0.1:8000 in browser.

##Settings

Settings File (settings.py)

PROXY: A tuple of proxy host and port. PROXIES, PROXY_HOST, PROXY_PORT is manipulated by this.

CACHE_DIR: The directory to store ONLY cache picture file. Illust info and tokens are store in script folder with extension ".pkl"
