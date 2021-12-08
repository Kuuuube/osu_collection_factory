import json
import subprocess

from pathlib import Path

from util import get_json_response


# TODO cache the id - hash pairs locally

def id_to_db(map_ids: set, api_key: str):
    with open("../settings.json", "r") as f:
        data = json.load(f)

    filepath = Path(data["output_collection_path"]).joinpath(data["output_collection_name"])

    url = "https://osu.ppy.sh/api/get_beatmaps"
    for map_id in map_ids:
        payload = {
            'k': api_key,
            'b': map_id,
            'type': 'id',
            'limit': 100,
        }

        if len(map_id) > 0:
            beatmap_json = get_json_response(url, payload)

            with open(filepath, 'a') as f:
                f.write(",," + beatmap_json["file_md5"] + "\n")

            print(f"ID: {map_id} MD5: {beatmap_json['file_md5']}")  # TODO log this

    subprocess.check_call([r"CollectionCSVtoDB\CollectionCSVtoDB.exe", str(filepath) + ".csv",
                           str(filepath) + ".db"])
