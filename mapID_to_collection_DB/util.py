import json
import os
import shutil
import time
from pathlib import Path

import requests

from typing import Any, NoReturn
from json import JSONDecodeError
from requests.exceptions import HTTPError

JSON = dict[str, Any]


# TODO log errors
# TODO should be able to detect if its an invalid beatmap id/set id
def get_json_response(url: str, payload: dict[str, Any], rate_limit: float | None = 1) -> JSON | NoReturn:
    try:
        r = requests.get(url, params=payload)

        # Raises exception if status code is not 200
        r.raise_for_status()

        try:
            r_json = r.json()

        # Raised if json received is invalid
        except JSONDecodeError:
            print("JSON decoding failed")
            quit(1)

        except Exception as e:
            print(f"An unknown error occurred: {e}")
            quit(1)

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        quit(1)

    # If other exception is raised
    except Exception as e:
        print(f"An unknown error occurred: {e}")
        quit(1)

    # Ratelimiting (~60/min)
    time.sleep(rate_limit)

    # noinspection PyUnboundLocalVariable
    return r_json


def change_default_collection_output_name() -> None:
    output_collection_name = input("Enter new collection name: ")

    with open("settings.json", "r") as f:
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

    with open("settings.json", "w") as f:
        data["output_collection_name"] = output_collection_name
        json.dump(data, f, indent=4)


def change_default_collection_output_path() -> None:
    output_collection_path = input("Enter new collection path: ")

    with open("settings.json", "r") as f:
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

    with open("settings.json", "w") as f:
        data["output_collection_path"] = output_collection_path
        json.dump(data, f, indent=4)
