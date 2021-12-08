import json
import subprocess
from pathlib import Path

from typing import NoReturn, Literal

from util import get_json_response

filter_menu = """\r
1) By star rating
2) By bpm
"""


def osu_collector_dump():
    min_sr_filter, max_sr_filter = None, None
    min_bpm_filter, max_bpm_filter = None, None

    collection_id = input("Enter collection ID or URL: ").split("/")[-1]  # TODO is there a way to validate this

    # If user wants to sort by diff
    # noinspection PyUnusedLocal
    use_filter = None
    while (use_filter := input("Filter collection? [y/n]: ").strip().lower()) not in ('y', 'n'):
        print(f"Not a valid input: {use_filter}")

    if use_filter == 'y':
        print(filter_menu)

        # noinspection PyUnusedLocal
        user_input = None
        while (user_input := input(">")) not in ('1', '2'):
            print(f"Invalid input: {user_input}")

        match user_input:
            case '1':
                # Get and sanity check min sr
                _min_sr_filter = None
                while _min_sr_filter is None:
                    _min_sr_filter = _filter_verification(filter_name="star rating", sort="min")

                    if _min_sr_filter < 0:  # makes sure the filter is positive
                        print(f"Invalid star rating: {_min_sr_filter} - must be greater or equal to 0")
                        _min_sr_filter = None

                min_sr_filter = _min_sr_filter

                # Get and sanity check max sr
                max_sr_filter = _filter_verification(filter_name="star rating", sort="max")

            case '2':
                # Get and sanity check min bpm
                _min_bpm_filter = None
                while _min_bpm_filter is None:
                    _min_bpm_filter = _filter_verification(filter_name="bpm", sort="min")

                    if _min_bpm_filter < 0:  # makes sure the filter is positive
                        print(f"Invalid bpm: {_min_bpm_filter} - must be greater or equal to 0")
                        _min_bpm_filter = None

                min_bpm_filter = _min_bpm_filter

                # Get and sanity check max bpm
                max_bpm_filter = _filter_verification(filter_name="bpm", sort="max")

        _collector_dump_with_filter(collection_id, min_sr_filter, max_sr_filter, min_bpm_filter, max_bpm_filter)

    else:
        _collector_dump(collection_id)


def _filter_verification(filter_name: str, sort: Literal["min"] | Literal["max"]) -> float | None:
    f = None
    while f is None:
        f = input(f"{sort.capitalize()} {filter_name}: ")

        if f.strip() == "":
            f = 0
            return f

        try:
            f = float(f)  # validates the filter by casting to float

        except ValueError:
            print(f"Invalid {filter_name}: {f} - must be a number")
            f = None

    return f


def _collector_dump(collection_id) -> NoReturn:
    # Defaults
    filepath = "list.txt"  # TODO send to log

    # Get user settings
    with open("../settings.json", 'r') as f:
        data = json.load(f)

    csv_filepath = Path(data["output_collection_path"]).joinpath(data["output_collection_name"] + ".csv")

    url = f"https://osucollector.com/api/collections/{collection_id}"

    # Make request for json
    collection = get_json_response(url=url)

    # Collect beatmap ids and checksums from the json
    beatmap_ids = []
    checksums = []
    for beatmap_set in collection["beatmapsets"]:
        for beatmap in beatmap_set["beatmaps"]:
            beatmap_ids.append(str(beatmap["id"]))
            checksums.append(beatmap["checksum"])

    # Dump ids
    with open(filepath, "a") as id_dump:  # TODO log this
        for beatmap_id in beatmap_ids:
            id_dump.write(beatmap_id + "\n")

    # Dump checksums
    with open(csv_filepath, "w") as hash_dump:  # TODO is csv needed to parse?
        for checksum in checksums:
            hash_dump.write(",," + checksum + "\n")

    subprocess.check_call([r"CollectionCSVtoDB\CollectionCSVtoDB.exe", csv_filepath,
                           Path(data["output_collection_path"]).joinpath(data["output_collection_name"] + ".db")])


def _collector_dump_with_filter(collection_id: int | str,
                                diff_filter_min: float | None = None, diff_filter_max: float | None = None,
                                bpm_filter_min: int | None = None, bpm_filter_max: int | None = None) -> NoReturn:
    # Defaults
    has_more = True
    cursor = "0"
    filepath = "list.txt"  # TODO send to log

    # Get user settings
    with open("../settings.json", 'r') as f:
        data = json.load(f)

    csv_filepath = Path(data["output_collection_path"]).joinpath(data["output_collection_name"] + ".csv")

    # Filter booleans
    using_diff_filter = diff_filter_min is not None or diff_filter_max is not None or diff_filter_max == 0
    using_bpm_filter = bpm_filter_min is not None or bpm_filter_max is not None or bpm_filter_max == 0

    # Wipe csv file
    with open(csv_filepath, "w") as wipe_file:
        pass

    while has_more:
        if using_diff_filter:
            url = f"https://osucollector.com/api/collections/{collection_id}/beatmapsv2?"
            payload = {
                "cursor": cursor,
                "perPage": "100",
                "sortBy": "difficulty_rating",
                "filterMin": diff_filter_min if diff_filter_min is not None else 0,
                "filterMax": diff_filter_max
            }

        elif using_bpm_filter:
            url = f"https://osucollector.com/api/collections/{collection_id}/beatmapsv2?"
            payload = {
                "cursor": cursor,
                "perPage": "100",
                "sortBy": "bpm",
                "filterMin": bpm_filter_min if bpm_filter_min is not None else 0,
                "filterMax": bpm_filter_max
            }

        else:
            raise NotImplementedError("Filter not supported")

        # Make request for json
        collection = get_json_response(url=url, payload=payload)

        # Collect beatmap ids and checksums from the json
        beatmap_ids = []
        checksums = []
        for beatmap in collection["beatmaps"]:
            beatmap_ids.append(beatmap["url"].split("/")[-1])
            checksums.append(beatmap["checksum"])

        # Dump ids
        with open(filepath, "a") as id_dump:  # TODO log this
            for beatmap_id in beatmap_ids:
                id_dump.write(beatmap_id + "\n")

        # Dump checksums
        with open(csv_filepath, "a") as hash_dump:  # TODO is csv needed to parse?
            for checksum in checksums:
                hash_dump.write(",," + checksum + "\n")

        # If more is available to request
        has_more = collection["hasMore"]
        if has_more:
            cursor = collection["nextPageCursor"]
            print(f"next cursor={int(cursor)}")  # TODO log this

    subprocess.check_call([r"CollectionCSVtoDB\CollectionCSVtoDB.exe", csv_filepath,
                               Path(data["output_collection_path"]).joinpath(data["output_collection_name"] + ".db")])
