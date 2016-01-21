import json
import os

import tornado.ioloop
import tornado.web

from Pixiv import Pixiv

pixiv = Pixiv()


class GetFollowingHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        result = json.dumps(pixiv.get_following(args[0]))
        self.write(result)


if __name__ == '__main__':
    # pixiv.login()
    app = tornado.web.Application([
        (r'/get_following/(.*)', GetFollowingHandler),
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'static/'),
                                                   'default_filename': 'index.html'})
    ])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
