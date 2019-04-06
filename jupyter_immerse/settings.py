import json
import os

from jupyterlab_server.json_minify import json_minify

SETTINGS_FILE = 'jupyterlab-omnisci/connection.jupyterlab-settings'

def write_default_connection(connection, settings_dir):
    fn = os.path.join(settings_dir, SETTINGS_FILE)
    with open(fn) as f:
        raw = f.read()
        settings = json.loads(json_minify(raw))

    servers = settings["servers"]

    connection['master'] = False
    for server in servers:
        server['master'] = False
    
    match = None
    for server in servers:
        diff = [key for key, item in connection.items() if server.get(key) != item]
        if len(diff) == 0:
            match = server
            break

    if match:
        server['master'] = True
    else:
        connection['master'] = True
        servers.insert(0, connection)

    with open(fn, 'w') as f:
        f.write(json.dumps(settings, indent=2))
