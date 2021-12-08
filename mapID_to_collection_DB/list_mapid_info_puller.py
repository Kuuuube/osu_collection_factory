import json
import subprocess

from pathlib import Path

from util import get_json_response


# TODO cache the id - hash pairs locally

def id_to_db(map_ids: set, api_key: str):
    with open("../settings.json", "r") as f:
        data = json.load(f)

    filepath = Path(data["output_collection_path"]).joinpath(data["output_collection_name"])
    csv_filepath = str(filepath) + ".csv"
    db_filepath = str(filepath) + ".db"

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
            
            with open(csv_filepath, 'a') as f:
                f.write(",," + beatmap_json[0]["file_md5"] + "\n")

            print(f"ID: {map_id} MD5: {beatmap_json[0]['file_md5']}")  # TODO log this

    subprocess.check_call([r"CollectionCSVtoDB\CollectionCSVtoDB.exe", csv_filepath, db_filepath])
