import os
import json
import logging

from pathlib import Path
from string import Template
from dotenv import load_dotenv

import util
import parser
import osu_collector_dumper


# Starts logger
logging.basicConfig(format="[%(levelname)s] - %(asctime)s - %(name)s:\n%(message)s",
                    datefmt="%d-%b-%y %H:%M:%S",
                    filename="../log.txt",
                    filemode="w",
                    level=logging.INFO)
logging.info("Starting logging")

# Loads .env file for osu!api key if stored
load_dotenv()

main_menu = """\r
TITLE
----------------------------------------
1) Create collection from osu!collector
2) Create collection from file
3) Change collection settings
4) Quit
"""

settings_menu = Template("""\r
Settings
---------------------
1) Change output collection name: Current name $output_collection_name
2) Change output collection path: Current path $output_collection_path
3) Back
""")


def main():
    print(main_menu)

    # noinspection PyUnusedLocal
    user_choice = None
    while (user_choice := input("> ")) not in ("1", "2", "3", "4"):
        print(f"Invalid option {user_choice}")

    match user_choice:
        case '1':
            osu_collector_dumper.osu_collector_dump()
            main()
        case '2':
            parser.parse_file()
            main()
        case '3':
            settings()
        case '4':
            quit(0)
        case _:
            raise Exception("This shouldn't be reached")


def settings():
    with open("../settings.json", "r") as f:
        data = json.load(f)
        output_collection_name = data["output_collection_name"]
        output_collection_path = data["output_collection_path"]

    print(settings_menu.substitute(output_collection_name=output_collection_name,
                                   output_collection_path=output_collection_path))

    # noinspection PyUnusedLocal
    user_choice = None
    while (user_choice := input("> ")) not in ("1", "2", "3"):
        print(f"Invalid option {user_choice}")

    match user_choice:
        case '1':
            util.change_default_collection_output_name()
            settings()
        case '2':
            util.change_default_collection_output_path()
            settings()
        case '3':
            main()
        case _:
            raise Exception("This shouldn't be reached")


if __name__ == "__main__":
    # Writes default settings if 'settings.json' doesn't exist
    try:
        Path("../settings.json").resolve(strict=True)

    except (OSError, RuntimeError, FileNotFoundError):
        default_settings = {
            "output_collection_name": "Collection",
            "output_collection_path": ".."
        }

        with open("../settings.json", "w") as f:
            json.dump(default_settings, f, indent=4)

    main()
