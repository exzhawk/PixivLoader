import json

import tornado.ioloop
import tornado.web
from tornado import concurrent

from Pixiv import *


class GetFollowingHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        result = yield executor.submit(pixiv.get_following, args[0])
        self.write(json.dumps(result))
        pixiv.cache_pic(result)


class GetCacheImgHandler(tornado.web.StaticFileHandler):
    def parse_url_path(self, url_path):
        return quote(url_path, safe='')

    @gen.coroutine
    def get(self, path, include_body=True):
        abs_path = self.get_absolute_path(self.root, self.parse_url_path(path))
        for i in range(30):
            if os.path.isfile(abs_path):
                break
            else:
                print('sleep')
                yield gen.sleep(3)
        super(GetCacheImgHandler, self).get(path, include_body)

    @classmethod
    def get_content(cls, abspath, start=None, end=None):
        with open(abspath, "rb") as file:
            if start is not None:
                file.seek(start)
            if end is not None:
                remaining = end - (start or 0)
            else:
                remaining = None
            return file.read(remaining)


pixiv = Pixiv()
executor = concurrent.futures.ThreadPoolExecutor(10)

if __name__ == '__main__':
    settings = {'static_path': os.path.join(os.path.dirname(__file__), 'static/')}
    app = tornado.web.Application([
        (r'/get_following/(.*)', GetFollowingHandler),
        (r'/get_file/(.*)', GetCacheImgHandler, {'path': CACHE_DIR}),
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path'], 'default_filename': 'index.html'})
    ])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
