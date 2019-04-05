import copy
import json

import tornado.web as web

from notebook.base.handlers import APIHandler, IPythonHandler

from .config import ImmerseConfig
from .workspace import WORKSPACE_TEMPLATE, write_workspace


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

    def initialize(self, base_url, lab_url, workspaces_dir, workspaces_url):
        self.server_base = base_url
        self.lab_url = lab_url
        self.workspaces_dir = workspaces_dir
        self.workspaces_url = workspaces_url

    @web.authenticated
    def get(self):
        """
        Get the URL for JupyterLab.
        """
        self.set_status(200)
        self.finish({"url": self.lab_url})

    @web.authenticated
    def post(self):
        data = self.get_json_body()
        workspace = copy.deepcopy(WORKSPACE_TEMPLATE)
        query = data["query"]
        widget = workspace["data"]["omnisci-grid-widget:omnisci-grid-widget-1"]
        widget["data"]["initialQuery"] = query
        space_name = "omnisci"
        write_workspace(
            workspace,
            self.workspaces_dir,
            self.server_base,
            self.workspaces_url,
            space_name,
        )
        self.set_status(200)
        self.finish({"url": f"{self.workspaces_url}{space_name}"})


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
