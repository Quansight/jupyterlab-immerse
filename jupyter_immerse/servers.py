import json

import tornado.web as web

from notebook.base.handlers import IPythonHandler


class ImmerseServersHandler(IPythonHandler):

    @web.authenticated
    def get(self):
        resp = [
            {
                "GTM": "GTM-5SWDG4",
                "customStyles": {
                    "title": "OmniSci | Data Visualization Example / Demo: Shipping Traffic Demo"
                },
                "database": "mapd",
                "host": "ships-demo-local.mapd.com",
                "loadDashboard": "8",
                "master": True,
                "port": 443,
                "protocol": "https",
                "password": "HyperInteractive",
                "username": "demouser",
            }
        ]
        self.set_status(200)
        self.finish(json.dumps(resp))
