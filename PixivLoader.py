import json

import tornado.ioloop
import tornado.web

from Pixiv import *

pixiv = Pixiv()


class GetFollowingHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        result = json.dumps(pixiv.get_following(args[0]))
        self.write(result)


class GetCacheImgHandler(tornado.web.StaticFileHandler):
    def parse_url_path(self, url_path):
        return quote(url_path, safe='')


if __name__ == '__main__':
    pixiv.login()
    settings = {'static_path': os.path.join(os.path.dirname(__file__), 'static/'),}
    app = tornado.web.Application([
        (r'/get_following/(.*)', GetFollowingHandler),
        (r'/get_file/(.*)', GetCacheImgHandler, {'path': CACHE_DIR}),
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path'], 'default_filename': 'index.html'})
    ])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
