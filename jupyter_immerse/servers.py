import json

from traitlets.config import Configurable
from traitlets import Dict, List, default


class BaseImmerseServersManager(Configurable):
    """
    A class managing getting and setting of default server
    connection data for connections to OmniSci backends.
    """

    def get_servers(self):
        return []

    def set_servers(self):
        raise NotImplementedError(
            "This manager does not support setting server connections"
        )


class ImmerseServersManager(BaseImmerseServersManager):
    """
    An Immerse servers manager that gets and sets the servers.json
    file from a static file.
    """
    servers = List(
        Dict,
        None,
        help="""
            Dictionary for OmniSci servers to be specified via notebook server
            config. If this is not None, then the manager will use the servers
            specified in the file specified by the path
            argument in the constructor.
            """,
        config=True,
        allow_none=True,
    )

    @default("servers")
    def _default_servers(self):
        return None

    def __init__(self, path, **kwargs):
        super(BaseImmerseServersManager, self).__init__(**kwargs)
        self.path = path

    def get_servers(self):
        if self.servers:
            return self.servers

        with open(self.path) as f:
            data = f.read()
            return json.loads(data)
