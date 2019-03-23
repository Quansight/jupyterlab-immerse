from traitlets import Unicode, Instance, default
from traitlets.config import Configurable

from .servers import BaseImmerseServersManager, ImmerseServersManager


class ImmerseConfig(Configurable):
    """
    Allows configuration of access to Immerse 
    """
    immerse_dir = Unicode(
        "./dist", config=True, help="The path to the built Immerse application"
    )
    immerse_servers_manager = Instance(
        BaseImmerseServersManager,
        config=True,
        help="A manager instance that knows how to get and set default OmniSci servers for immerse",
    )

    @default("immerse_servers_manager")
    def _default_immerse_servers_manager(self):
        """
        Default to the servers.json in the immerse static directory.
        """
        return ImmerseServersManager(f"{self.immerse_dir}/servers.json")
