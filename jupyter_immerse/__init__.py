from tornado.web import StaticFileHandler
from traitlets import Unicode
from traitlets.config import Configurable

from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler

__version__ = "0.1.0"


class ImmerseConfig(Configurable):
    """
    Allows configuration of access to Immerse 
    """
    immerse_dir = Unicode(
        "./dist",
        config=True,
        help="The path to the built Immerse application",
    )


class ImmerseHandler(StaticFileHandler):
    def get(self, path):
        path = path.strip("/")
        return StaticFileHandler.get(self, path)


def _jupyter_server_extension_paths():
    return [{"module": "jupyterlab_immerse"}]


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    c = ImmerseConfig(config=nb_server_app.config)
    web_app = nb_server_app.web_app
    base_url = web_app.settings["base_url"]
    endpoint = url_path_join(base_url, "immerse")
    handlers = [
        (
            endpoint + "(.*)",
            ImmerseHandler,
            {"path": c.immerse_dir, "default_filename": "index,html"},
        )
    ]
    web_app.add_handlers(".*$", handlers)
