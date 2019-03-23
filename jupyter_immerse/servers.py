import json

from traitlets.config import Configurable


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

    def __init__(self, path):
        self.path = path

    def get_servers(self):
        with open(self.path) as f:
            data = f.read()
            return json.loads(data)
