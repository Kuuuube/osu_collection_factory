import json
import logging

from pathlib import Path

logger = logging.getLogger(__name__)


def convert_md5s_to_db(md5s: set):
    with open("../settings.json", "r") as d:
        data = json.load(d)
        name = data["output_collection_name"]

    path = Path(data["output_collection_path"]).joinpath(name + ".db")

    logger.info("Starting MD5 to DB conversion")

    with open(path, "wb") as f:
        f.write(b"\x00\x00\x00\x00")  # arbitrary osu! version
        f.write((1).to_bytes(4, "little"))  # number of collections
        f.write(b"\x0b")  # spacer
        f.write(len(name).to_bytes(1, "little"))
        f.write(name.encode())  # name of collection
        f.write(len(md5s).to_bytes(4, "little"))  # length of collection
        for md5 in md5s:
            f.write(b"\x0b ")  # spacer
            f.write(md5.encode())  # md5

    logger.info("MD5 to DB conversion successful")
