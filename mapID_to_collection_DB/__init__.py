import json

from pathlib import Path

try:
    import requests

except ImportError:
    raise ImportError("'Requests' module not found (Try running 'pip install requests')")

try:
    Path("settings.json").resolve()

except (OSError, RuntimeError):
    with open("settings.json", 'w') as f:
        data = {
            "output_collection_name": "Collection.db",
            "output_collection_path": "."
        }

        json.dumps(data, indent=4)
