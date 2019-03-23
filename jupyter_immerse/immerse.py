import tornado.web as web

from notebook.base.handlers import IPythonHandler

class ImmerseHandler(IPythonHandler, web.StaticFileHandler):

    @web.authenticated
    def get(self, path):
        path = path.strip("/")
        return web.StaticFileHandler.get(self, path)
