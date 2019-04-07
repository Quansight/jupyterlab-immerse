import copy
import json
import os
import urllib

from jupyterlab_server.json_minify import json_minify

SETTINGS_FILE = 'jupyterlab-omnisci/connection.jupyterlab-settings'

def write_default_connection(connection, settings_dir, immerse_servers=[]):
    fn = os.path.join(settings_dir, SETTINGS_FILE)
    with open(fn) as f:
        raw = f.read()
        settings = json.loads(json_minify(raw))

    lab_servers = settings["servers"]

    # Set all the known servers master attribute to false.
    # We will then look for matches if one is found, it
    # will become the master server.
    connection['master'] = False
    for server in lab_servers:
        server['master'] = False
    for server in immerse_servers:
        server['master'] = False
    
    lab_match = None
    immerse_match = None
    for server in lab_servers:
        if _maybe_same(connection, server):
            lab_match = server
            break
    for server in immerse_servers:
        if _maybe_same(connection, server):
            immerse_match = server
            break

    print(lab_match, immerse_match)
    if lab_match:
        lab_match['master'] = True
    elif immerse_match:
        immerse_match['master'] = True
        lab_servers.insert(0, immerse_match)
    else:
        connection['master'] = True
        lab_servers.insert(0, connection)

    with open(fn, 'w') as f:
        f.write(json.dumps(settings, indent=2))

def _maybe_same(a, b):
    a = _normalize_server(a)
    b = _normalize_server(b)
    diff = [key for key, item in a.items() if b.get(key) != item]
    return len(diff) == 0

def _normalize_server(s):
    s = copy.deepcopy(s)
    if s.get("url"):
        parsed = urllib.parse.urlparse(s["url"])
        s["host"] = parsed.hostname
        s["port"] = parsed.port
        s["protocol"] = parsed.scheme
        s.pop("url")
    return s
