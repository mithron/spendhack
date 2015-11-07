import json
import os
from urllib import parse as urlparse
import pymongo

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.template import Loader
import tornado.log

from tornado.options import define, options


MONGO_URL = "" # found with $>heroku config
we_live = True

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", SearchHandler),
            (r"/result/", OutputHandler)
        ]
        settings = dict(
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.con = pymongo.MongoClient('localhost', 27017)
        self.db = self.con["meanspend"]
        self.col = self.db['data']
        self.templates = Loader("web")

class BaseHandler(tornado.web.RequestHandler):
    @property
    def col(self):
        return self.application.col
        
    def templates(self):
        return self.application.templates


class OutputHandler(BaseHandler):
    def get(self, fname=None):
        print(str(fname))
        if fname:
            data2 = self.col.find_one({'$or': [{'name': str(fname)}, {'code': str(fname)}] })
            print('!!!!!!!!!!!!!!!!!!')
            self.write(self.templates().load("output.html").generate(data))
        else:
            data2 = self.col.find_one({'code': '28.63.12.119'})
        self.write(self.templates().load("output.html").generate(data = data2))
        
    def post(self, fname=None):
        print(str(fname))
        if fname:
            data2 = self.col.find_one({'$or': [{'name': str(fname)}, {'code': str(fname)}] })
            print('!!!!!!!!!!!!!!!!!!')
            self.write(self.templates().load("output.html").generate(data))
        else:
            data2 = self.col.find_one({'code': '28.63.12.119'})
        self.write(self.templates().load("output.html").generate(data = data2))

class SearchHandler(BaseHandler):
    def get(self):
     
        self.write(self.templates().load("input.html").generate(title = "Поиск по коду ОКДБ или наименованию"))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(int(os.environ.get("PORT", 8888)))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()