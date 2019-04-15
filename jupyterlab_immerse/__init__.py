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

    # Holy traitlets
    base_url = web_app.settings["base_url"]
    workspaces_dir = nb_server_app.workspaces_dir
    settings_dir = nb_server_app.user_settings_dir
    workspaces_url = lab_config.workspaces_url
    lab_url = lab_config.page_url

    immerse_endpoint = url_path_join(base_url, "immerse")
    servers_endpoint = url_path_join(base_url, "immerse", "servers.json")
    lab_redirect_endpoint = url_path_join(base_url, "immerse", "lab")
    handlers = [
        (servers_endpoint, ImmerseServersHandler),
        (
            lab_redirect_endpoint,
            ImmerseLabRedirectHandler,
            {
                "base_url": base_url,
                "lab_url": lab_url,
                "settings_dir": settings_dir,
                "workspaces_dir": workspaces_dir,
                "workspaces_url": workspaces_url,
            },
        ),
        (
            immerse_endpoint + "(.*)",
            ImmerseHandler,
            {"path": immerse_config.immerse_dir, "default_filename": "index.html"},
        ),
    ]
    web_app.add_handlers(".*$", handlers)
