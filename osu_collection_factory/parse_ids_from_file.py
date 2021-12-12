import os
import re
import logging

from os import PathLike
from pathlib import Path

from util import get_json_response
from md5_conversion import convert_md5s_to_db
from set_id_to_map_ids import set_id_list_to_map_id_list

# TODO locally cache set_id -> map_id -> md5

logger = logging.getLogger(__name__)


def parse_file():
    path_to_file = input("Enter file to parse (Default - list.txt): ")

    if path_to_file == "":
        path_to_file = "../list.txt"  # Grab from parent directory

    # Sanity check path
    try:
        path_to_file = Path(path_to_file).resolve(strict=True)

    except (RuntimeError, OSError):
        logger.error(f"Invalid path given: {path_to_file}")
        raise Exception(f"Invalid path: {path_to_file}")

    # Try getting api key from .env
    potential_key = os.getenv("KEY")

    if potential_key is None:
        api_key = input("Enter osu! API key: ")

    else:
        api_key = potential_key

    id_dict = _parse_ids(path_to_file)

    map_ids_set = set_id_list_to_map_id_list(set_ids=id_dict["set_ids"], api_key=api_key)

    if len(id_dict["map_ids"]) != 0:
        for m in id_dict["map_ids"]:
            map_ids_set.add(m)

    id_to_md5(map_ids_set, api_key)


def _parse_ids(path_to_file: PathLike | str) -> dict[str, set]:
    # Defaults
    map_ids = set()
    set_ids = set()

    with open(path_to_file, "r", encoding='utf8') as f:
        f_lines = f.readlines()
    content = list(map(str.strip, f_lines))

    # Regex pattern to pull osu.ppy.sh/s/* links
    pattern = re.compile(r'(((http.{0,4})?osu\.ppy\.sh/(?!u)\w{1,11}/((\d{1,8})?((#|%23)\w{1,5}/\d{1,8}|\w{1,7}\?b=\d{'
                         r'1,8}(&m=\d)?)|\d{1,8}))|(^\d{1,8}))')
    # Regex pattern to pull set IDs if no map ID is specified
    set_id_pattern = re.compile(r"((?!(?<=ets/)\d{1,7}(#|%23))((?<=s/)\d{1,7}))")
    # Regex pattern to pull map IDs
    map_id_pattern = re.compile(r"(((?<!ets/)(?<!/s/)(?<=\w/)\d{1,8}|^\d{1,8}))")
    # Regex pattern for raw map IDs
    raw_map_id_pattern = re.compile(r"")

    for line in content:
        for link in pattern.finditer(line):
            set_id = re.search(set_id_pattern, link.group(0))

            # Only append if set ID is found without map ID
            if set_id is not None:
                logger.info(f'Possible set ID found: {set_id.group(0)}')
                set_ids.add(set_id.group(0))

            else:
                map_id = re.search(map_id_pattern, link.group(0))

                # Only append if map ID is found
                if map_id is not None:
                    logger.info(f'Possible map ID found: {map_id.group(0)}')
                    map_ids.add(map_id.group(0))

                else:
                    logger.warning(f"Invalid link? : {link.group(0)}")

    return {"set_ids": set_ids, "map_ids": map_ids}


def id_to_md5(map_ids: set, api_key: str):
    md5s = set()
    url = "https://osu.ppy.sh/api/get_beatmaps"

    for map_id in map_ids:
        payload = {
            'k': api_key,
            'b': map_id,
            'type': 'id',
            'limit': 100,
        }

        if len(map_id) > 0:
            try:
                beatmap_json = get_json_response(url, payload)

                md5s.add(beatmap_json[0]["file_md5"])

                logger.info(f"ID: {map_id} MD5: {beatmap_json[0]['file_md5']}")

            except IndexError:
                # Real funky workaround if map ID received is actually a set ID
                logger.info(f"Trying to interpret {map_id} as set ID")

                fixed_ids = set_id_list_to_map_id_list({map_id}, api_key)

                for fixed_id in fixed_ids:
                    md5s.add(fixed_id)

            except Exception as e:
                logger.exception(e)
                print(f"An error occurred: {e}")
                print(f"Create db from {len(md5s)} md5s? (y/n): ")

                user_input = None
                while (user_input := input()) not in ("y", "n"):
                    print(f"Invalid user input: {user_input}")

                if user_input == "y":
                    break

                else:
                    quit(1)

    convert_md5s_to_db(md5s)
