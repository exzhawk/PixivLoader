import json

import tornado.ioloop
import tornado.web

from Pixiv import *


class GetFollowingHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        result = pixiv.get_following(args[0])
        self.write(json.dumps(result))
        pixiv.cache_pic(result)


class GetCacheImgHandler(tornado.web.StaticFileHandler):
    def parse_url_path(self, url_path):
        return quote(url_path, safe='')


pixiv = Pixiv()
if __name__ == '__main__':
    settings = {'static_path': os.path.join(os.path.dirname(__file__), 'static/'),}
    app = tornado.web.Application([
        (r'/get_following/(.*)', GetFollowingHandler),
        (r'/get_file/(.*)', GetCacheImgHandler, {'path': CACHE_DIR}),
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path'], 'default_filename': 'index.html'})
    ])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
