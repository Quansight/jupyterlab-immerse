from traitlets import Unicode
from traitlets.config import Configurable

class ImmerseConfig(Configurable):
    """
    Allows configuration of access to Immerse 
    """
    immerse_dir = Unicode(
        "./dist", config=True, help="The path to the built Immerse application"
    )
