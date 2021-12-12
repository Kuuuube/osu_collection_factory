import os
import json
import time
import shutil
import logging
import requests

from pathlib import Path
from json import JSONDecodeError
from typing import Any, NoReturn
from requests.exceptions import HTTPError


# Constants
JSON = dict[str, Any]
JSON_LIST = list[JSON]

logger = logging.getLogger(__name__)


# TODO log errors
# TODO should be able to detect if its an invalid beatmap id/set id
def get_json_response(url: str, payload: dict[str, Any] | None = None, rate_limit: float | None = 1)\
        -> JSON | JSON_LIST | NoReturn:
    try:
        r = requests.get(url, params=payload)
        r.raise_for_status()

        try:
            r_json = r.json()

        # Raised if json received is invalid
        except JSONDecodeError:
            logger.error("JSON decoding failed")
            raise Exception("JSON decoding failed")

        except Exception as e:
            logger.error(f"An unknown error occurred: {e}")
            raise Exception(f"An unknown error occurred: {e}")

    # Raised if HTTP status code is not 200
    except HTTPError as http_err:
        # noinspection PyUnboundLocalVariable
        if r.status_code == 401 and url.startswith("https://osu.ppy.sh"):
            logger.error("Invalid osu!api key used")
            raise HTTPError("Invalid osu!api key used")

        logger.error(f"HTTP error occurred: {http_err}")
        raise HTTPError(f"HTTP error occurred: {http_err}")

    except Exception as e:
        logger.error(f"An unknown error occurred: {e}")
        raise Exception(f"An unknown error occurred: {e}")

    # Ratelimiting (~60/min)
    time.sleep(rate_limit)

    # noinspection PyUnboundLocalVariable
    return r_json


def change_default_collection_output_name() -> None:
    output_collection_name = input("Enter new collection name: ")

    with open("../settings.json", "r") as f:
        data = json.load(f)

    collection_path = data["output_collection_path"]

    # Removes extension if needed
    if output_collection_name.endswith(".db"):  # or ...
        output_collection_name = output_collection_name.replace(".db", "")

    # noinspection PyUnusedLocal
    user_input = None
    while (user_input := input("Rename current collection? (y/n): ")) not in ('y', 'n'):
        print(f"Invalid input: {user_input}")

    if user_input == 'y':
        os.rename(Path(collection_path).joinpath(data["output_collection_name"] + ".db"),
                  Path(collection_path).joinpath(output_collection_name + ".db"))

    with open("../settings.json", "w") as f:
        data["output_collection_name"] = output_collection_name
        json.dump(data, f, indent=4)

    logger.info(f"output_collection_name changed to: {output_collection_name}")


# TODO should ask if user wants to create new dir
def change_default_collection_output_path() -> None:
    output_collection_path = input("Enter new collection path: ")

    with open("../settings.json", "r") as f:
        data = json.load(f)

    collection_name = data["output_collection_name"]

    if not Path(output_collection_path).is_dir():
        print(f"Invalid dir: {output_collection_path}")
        return

    try:
        Path(output_collection_path + collection_name)

    except(OSError, RuntimeError):
        pass

    finally:
        # noinspection PyUnusedLocal
        user_input = None
        while (user_input := input("Move current collection to new Path? (y/n): ")) not in ('y', 'n'):
            print(f"Invalid input: {user_input}")

        if user_input == 'y':
            shutil.move(Path(data["output_collection_path"]).joinpath(collection_name + ".db"),
                        Path(output_collection_path).joinpath(collection_name + ".db"))

    with open("../settings.json", "w") as f:
        data["output_collection_path"] = output_collection_path
        json.dump(data, f, indent=4)

    logger.info(f"output_collection_path changed to: {output_collection_path}")
