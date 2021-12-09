import json

from pathlib import Path

from parser import parse_file
from list_mapid_info_puller import id_to_db
from md5_conversion import convert_md5s_to_db
from osu_collector_dumper import osu_collector_dump, osu_collector_dump_with_filter
from util import get_json_response, get_osu_api_json_response,\
    change_default_collection_output_name, change_default_collection_output_path

try:
    import requests

except ImportError:
    raise ImportError("'Requests' module not found (Try running 'pip install requests')")

try:
    import dotenv

except ImportError:
    raise ImportError("'Dotenv' module not found (Try running 'pip install python-dotenv')")

try:
    Path("settings.json").resolve(strict=True)

except (OSError, RuntimeError):
    with open("../settings.json", 'w') as f:
        data = {
            "output_collection_name": "Collection",
            "output_collection_path": ".."
        }

        json.dumps(data, indent=4)
