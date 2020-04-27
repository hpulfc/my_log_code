# coding=utf8
# Time    : 2020/4/15 11:45
# File    : ts.py
# Software: PyCharm
from tornado.httpserver import HTTPServer
from tornado.web import Application
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop


class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        print("body", self.request.body)
        print("argument", self.request.arguments)
        resp = {
            "a":1
        }
        # self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Origin", "http://localhost:63342")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_status(200)
        self.write(resp)

    def post(self, *args, **kwargs):
        resp = {

        }
        self.write(resp)


def get_app():
    app = Application(
        [
            (r'/', IndexHandler),
        ]
    )

    return app


if __name__ == '__main__':
    app = get_app()
    http_server = HTTPServer(app)
    http_server.listen("8080")
    print("start 8080 ...")
    IOLoop.current().start()
