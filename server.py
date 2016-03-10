"""
    Wraps the flask app in a tornado server. Tornado is fast too.
    Can handle tons of open connections all at once.
"""
__author__ = 'austin'

import os
import argparse
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application


class MainHandler(RequestHandler):
    def get(self):
        self.write("Y u want our tornado huh")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The vets 4 warriors frontend runner')
    parser.add_argument('-e', '--env', help="Either 'local', 'dev' or 'prod'. Default is 'prod'", required=True)
    args = parser.parse_args()

    os.environ['VETS_ENV'] = args.env

    # Now load the app
    from app import app as api
    flask = WSGIContainer(api)
    application = Application(
        [
            #
            (r"/tornado", MainHandler),
            # Send all others to flask
            (r".*", FallbackHandler, dict(fallback=flask)),
        ]
    )

    application.listen(8000)
    IOLoop.instance().start()
