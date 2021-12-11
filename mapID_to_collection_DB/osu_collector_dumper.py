import json
import logging

from typing import NoReturn, Literal

from md5_conversion import convert_md5s_to_db
from util import get_json_response

logger = logging.getLogger(__name__)

filter_menu = """\r
1) By star rating
2) By bpm
"""


def osu_collector_dump():
    # If user wants to sort beatmaps
    # noinspection PyUnusedLocal
    use_filter = None
    while (use_filter := input("Filter collection? [y/n]: ").strip().lower()) not in ("y", "n"):
        print(f"Not a valid input: {use_filter}")

    if use_filter == "y":
        osu_collector_dump_with_filter()

    else:
        collection_id = input("Enter collection ID or URL: ").split("/")[-1]  # TODO possibly cache this?
        _collector_dump(collection_id)


def osu_collector_dump_with_filter():
    min_sr_filter, max_sr_filter = None, None
    min_bpm_filter, max_bpm_filter = None, None

    collection_id = input("Enter collection ID or URL: ").split("/")[-1]

    print(filter_menu)

    # noinspection PyUnusedLocal
    user_input = None
    while (user_input := input(">")) not in ("1", "2"):
        print(f"Invalid input: {user_input}")

    match user_input:
        case "1":

            # Get and sanity check min sr
            min_sr_filter = _filter_verification(filter_name="star rating", sort="min")

            # Get and sanity check max sr
            max_sr_filter = _filter_verification(filter_name="star rating", sort="max")

        case "2":

            # Get and sanity check min bpm
            min_bpm_filter = _filter_verification(filter_name="bpm", sort="min")

            # Get and sanity check max bpm
            max_bpm_filter = _filter_verification(filter_name="bpm", sort="max")

    _collector_dump_with_filter(collection_id, min_sr_filter, max_sr_filter, min_bpm_filter, max_bpm_filter)


def _filter_verification(filter_name: str, sort: Literal["min"] | Literal["max"]) -> float | None:
    f = None
    while f is None:
        f = input(f"{sort.capitalize()} {filter_name}: ")
        if f.strip() == "":
            if sort == "min":
                return 0
            elif sort == "max":
                print(f"Invalid max {filter_name}: {f} - must be a number")
                f = None
                continue
        try:
            f = float(f)  # Validates the filter by casting to float
        except ValueError:
            print(f"Invalid {filter_name}: {f} - must be a number")
            f = None
            continue
        if f is not None and f < 0:  # Make sure filter is positive
            print(f"Invalid {filter_name}: {f} - must be greater or equal to 0")
            f = None
            continue
    return f


def _collector_dump(collection_id) -> NoReturn:
    # Defaults
    beatmap_ids = set()
    md5s = set()

    logger.info(f"Collecting beatmaps from osu!Collector collection {collection_id}:")

    url = f"https://osucollector.com/api/collections/{collection_id}"
    collection = get_json_response(url=url)

    # Collect beatmap ids and checksums from the json
    for beatmap_set in collection["beatmapsets"]:
        for beatmap in beatmap_set["beatmaps"]:
            beatmap_ids.add(str(beatmap["id"]))
            md5s.add(beatmap["checksum"])

    # Log ids
    for i, j in zip(beatmap_ids, md5s):
        logger.info(f"Dumped id: {i} - md5: {j}")
    logger.info("Collected successfully\n")

    # Dump checksums
    convert_md5s_to_db(md5s)


def _collector_dump_with_filter(collection_id: int | str,
                                diff_filter_min: float | None = None, diff_filter_max: float | None = None,
                                bpm_filter_min: int | None = None, bpm_filter_max: int | None = None) -> NoReturn:
    # Defaults
    has_more = True
    cursor = "0"
    md5s = set()
    beatmap_ids = set()

    # Filter booleans
    using_diff_filter = diff_filter_min is not None or diff_filter_max is not None or diff_filter_max == 0
    using_bpm_filter = bpm_filter_min is not None or bpm_filter_max is not None or bpm_filter_max == 0

    logger.info(f"Collecting beatmaps from osu!Collector collection {collection_id}:")
    if using_diff_filter:
        logger.info(f"Using star rating filter: {diff_filter_min}->{diff_filter_max}")
    elif using_bpm_filter:
        logger.info(f"Using bpm filter: {bpm_filter_min}->{bpm_filter_max}")
    else:
        logger.warning("Using unknown filter")

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
            logger.error("Unsupported filter used")
            raise NotImplementedError("Filter not supported")

        collection = get_json_response(url=url, payload=payload)

        # Collect beatmap ids and checksums from the json
        for beatmap in collection["beatmaps"]:
            beatmap_ids.add(beatmap["url"].split("/")[-1])
            md5s.add(beatmap["checksum"])

        # Log ids
        for i, j in zip(beatmap_ids, md5s):
            logger.info(f"Dumped id: {i} - md5: {j}")

        # If more is available to request
        has_more = collection["hasMore"]
        if has_more:
            cursor = collection["nextPageCursor"]

            # Log cursor
            logger.info(f"Next cursor: {cursor}")

    logger.info("Collected successfully\n")

    # Dump checksums
    convert_md5s_to_db(md5s)
