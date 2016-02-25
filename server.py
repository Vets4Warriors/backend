"""
    Wraps the flask app in a tornado server. Tornado is fast too.
    Can handle tons of open connections all at once.
"""
__author__ = 'austin'

from app import app as api

from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
import tornado.options


class MainHandler(RequestHandler):
    def get(self):
        self.write("Y u want our tornado huh")

flask = WSGIContainer(api)

application = Application(
    [
        #
        (r"/tornado", MainHandler),
        # Send all others to flask
        (r".*", FallbackHandler, dict(fallback=flask)),
    ]
)

if __name__ == "__main__":
    application.listen(8000)
    IOLoop.instance().start()
