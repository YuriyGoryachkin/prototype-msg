import tornado.web
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
from tornado.options import define, options
from handlers.json_util import BaseHandler
from handlers.mainhandlers import MainHandlers
from handlers.grouphandlers import GroupHandlers
from handlers.testhandlers import TestHandlers
from handlers.contacthandlers import ContactHandlers
from handlers.chathandlers import ChatHandlers
from handlers.userhandlers import UserHandlers

from database_tools.db_connect import Session

define("port", default=8888, help="start on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self, db=None):
        if db == None:
            db = Session()
        self.webSocketsPool = []
        handlers = [
            (r'/', Main),
            (r'/main/', MainHandlers),
            (r'/group/', GroupHandlers),
            (r'/contact/', ContactHandlers),
            (r'/chat/', ChatHandlers),
            (r'/user/', UserHandlers),
            (r'/test/', TestHandlers)
        ]

        # если понадобится cookie_secret(для подписания cookie),
        # login_url(декоратор для перенаправления на страницу авторизации не зарегистрированного пользователя
        settings = dict()
        # websocket_ping_interval=1 (для включения пинга) для отключение неактивных клиентов
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = db


class Main(BaseHandler):
    def get(self):
        result = "Welcome to GYVMessenger"
        self.write(str(result))


def main():
    print('Start server')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutdown: KeyboardInterrupt")
