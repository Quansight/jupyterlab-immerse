from notebook.utils import url_path_join

from jupyterlab_server import LabConfig

from .config import ImmerseConfig
from .handlers import ImmerseHandler, ImmerseLabRedirectHandler, ImmerseServersHandler

__version__ = "0.1.0"


def _jupyter_server_extension_paths():
    return [{"module": "jupyterlab_immerse"}]


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    immerse_config = ImmerseConfig(config=nb_server_app.config)
    lab_config = LabConfig(config=nb_server_app.config)

    base_url = web_app.settings["base_url"]
    endpoint = url_path_join(base_url, "immerse")
    servers_endpoint = url_path_join(base_url, "immerse", "servers.json")
    lab_redirect_endpoint = url_path_join(base_url, "immerse", "lab")
    handlers = [
        (servers_endpoint, ImmerseServersHandler),
        (
            lab_redirect_endpoint,
            ImmerseLabRedirectHandler,
            {"lab_url": lab_config.page_url}
        ),
        (
            endpoint + "(.*)",
            ImmerseHandler,
            {"path": immerse_config.immerse_dir, "default_filename": "index.html"},
        ),
    ]
    web_app.add_handlers(".*$", handlers)
