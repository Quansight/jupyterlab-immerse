import json

import tornado.web as web

from notebook.base.handlers import APIHandler, IPythonHandler

from .config import ImmerseConfig


class ImmerseHandler(IPythonHandler, web.StaticFileHandler):
    """
    A static file handler that serves assets from the immerse build directory.
    """

    @web.authenticated
    def get(self, path):
        path = path.strip("/")
        self.set_cookie("license", "enterprise")
        return web.StaticFileHandler.get(self, path)


class ImmerseLabRedirectHandler(APIHandler):
    """
    A handler that redirects to a JupyterLab workspace.
    """

    def initialize(self, lab_url):
        self.lab_url = lab_url

    @web.authenticated
    def get(self):
        """
        Get the URL for JupyterLab.
        """
        self.set_status(200)
        self.finish({"url": self.lab_url})

    def post(self):
        data = self.get_json_body()
        self.set_status(200)
        self.finish({"url": self.lab_url})


class ImmerseServersHandler(APIHandler):
    """
    A handler that serves default OmniSci server connection data to the frontend.
    """

    @web.authenticated
    def get(self):
        """
        Get default server connection data.
        """

        # Create a config object
        c = ImmerseConfig(config=self.config)
        try:
            # Get default server data from the configured servers manager.
            servers = c.immerse_servers_manager.get_servers()
            self.set_status(200)
            self.finish(json.dumps(servers))
        except Exception as e:
            self.set_status(500)
            self.finish(e)
