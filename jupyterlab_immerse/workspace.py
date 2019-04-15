import json
import os

from notebook.utils import url_path_join as ujoin
from jupyterlab_server.workspaces_handler import slugify, WORKSPACE_EXTENSION

fn = os.path.join(os.path.dirname(__file__), "workspace_template.jupyterlab-workspace")

with open(fn) as f:
    WORKSPACE_TEMPLATE = json.load(f)


def write_workspace(data, directory, base_url, workspaces_url, space_name="omnisci"):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception:
            raise Exception("Cannot create workspaces directory")

    # Set the correct workspace ID for the name.
    workspace_id = ujoin(base_url, workspaces_url, space_name)
    data["metadata"] = {"id": workspace_id}

    slug = slugify(workspace_id, base_url)
    workspace_path = os.path.join(directory, slug + WORKSPACE_EXTENSION)

    with open(workspace_path, "w") as out:
        out.write(json.dumps(data))

    return space_name
