from notebook.utils import url_path_join

from .config import ImmerseConfig
from .handlers import ImmerseHandler, ImmerseServersHandler

__version__ = "0.1.0"

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
    servers_endpoint = url_path_join(base_url, "immerse", "servers.json")
    handlers = [
        (
            servers_endpoint,
            ImmerseServersHandler,
        ),
        (
            endpoint + "(.*)",
            ImmerseHandler,
            {"path": c.immerse_dir, "default_filename": "index.html"},
        ),
    ]
    web_app.add_handlers(".*$", handlers)
