import requests
import re
import time
import subprocess


def osu_collector_dump_diff(collection_id: int | str, collection_name: str,
                            diff_filter_min: int | None = None, diff_filter_max: int | None = None):
    has_more = True
    cursor = "0"
    filepath = "list.txt"

    # Remove extension and parse id from url if necessary
    collection_name_no_extension = re.sub(r"\..*", "", collection_name)

    if isinstance(collection_id, str):
        collection_id = collection_id.split("/")[-1]

    csv_filepath = f"{collection_name_no_extension}.csv"

    while has_more:
        # Default url and payload
        url = f"https://osucollector.com/api/collections/{collection_id}/beatmapsv2?"
        payload = {
            "cursor": cursor,
            "perPage": "100",
            "sortBy": "difficulty_rating"
        }

        # Filter logic
        # TODO implement bpm min/max (can only sort by one)
        if diff_filter_min is not None or diff_filter_max is not None:
            payload["filterMin"] = diff_filter_min if diff_filter_min is not None else 0
            payload["filterMax"] = diff_filter_max if diff_filter_max is not None else 0

        # Make request for json
        # TODO error handle this
        r = requests.get(url, payload)
        collection = r.json()

        # Collect beatmap ids and checksums from the json
        beatmap_ids = []
        checksums = []
        for beatmap in collection["beatmaps"]:
            beatmap_ids.append(beatmap["url"].split("/")[-1])
            checksums.append(beatmap["checksum"])

        # Dump ids
        with open(filepath, "a") as id_dump:
            for beatmap_id in beatmap_ids:
                id_dump.write(beatmap_id + "\n")

        # Dump checksums
        with open(csv_filepath, "w") as hash_dump:
            for checksum in checksums:
                hash_dump.write(checksum + "\n")

        # Api ratelimiting if more is available to request
        has_more = collection["hasMore"]
        if has_more:
            cursor = collection["nextPageCursor"]
            print("osu!Collector: waiting 5 seconds.")
            print(f"next cursor={int(cursor)}")
            time.sleep(5)

    subprocess.check_call([r"CollectionCSVtoDB\CollectionCSVtoDB.exe", csv_filepath, collection_name])
