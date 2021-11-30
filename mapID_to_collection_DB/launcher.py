import re
from os import PathLike

import osu_collector_dumper
import list_mapid_info_puller
import html_to_list
import setID_to_mapIDs

# TODO properly handle out_collection_path


def osu_collector_dump(out_collection_path: PathLike | str):
    min_sr_filter, max_sr_filter = None, None

    collection_id = input("Enter collection ID or URL: ")  # TODO is there a way to validate this

    # this checks if the input is valid, if it isn't, print it and loop back
    diff_filter = None
    while (diff_filter := input("Filter by star rating? [y/n]: ").strip().lower()) not in {'y', 'n'}:
        print(f"Not a valid input: {diff_filter}")

    if diff_filter == 'y':
        while min_sr_filter is None:
            min_sr_filter = input("Minimum star rating: ")

            try:
                min_sr_filter = float(min_sr_filter)  # validates the filter as a float

            except ValueError:
                print(f"Invalid star rating: {min_sr_filter} - must be a number")
                min_sr_filter = None

            if min_sr_filter < 0:  # makes sure the filter is positive
                print(f"Invalid star rating: {min_sr_filter} - must be greater or equal to 0")
                min_sr_filter = None

        while max_sr_filter is None:
            max_sr_filter = input("Maximum star rating: ")

            try:
                max_sr_filter = float(max_sr_filter)  # validates the filter as a float

            except ValueError:
                print(f"Invalid star rating: {max_sr_filter} - must be a number")
                max_sr_filter = None

    osu_collector_dumper.osu_collector_dump(collection_id, out_collection_path, min_sr_filter, max_sr_filter)

    # TODO allow osu.collector.dumper to accept diff filters with value None


def html_dump(out_collection_path: PathLike | str):
    html_path = input("Enter path to HTML/HTM file: ")  # TODO is there a way to validate this
    api_key = input("Enter API key: ")

    
    setID_to_mapIDs.setID_to_list(html_path)
    html_to_list.html_to_list(html_path)

    setID_to_mapIDs.setID_list_to_mapID_list(api_key)
    list_mapid_info_puller.id_to_db(api_key, out_collection_path)


def list_txt_dump(out_collection_path: PathLike | str):
    api_key = input("Enter API key: ")

    setID_to_mapIDs.setID_to_list("list.txt")
    html_to_list.html_to_list("list.txt")

    setID_to_mapIDs.setID_list_to_mapID_list(api_key)
    list_mapid_info_puller.id_to_db(api_key, out_collection_path)


if __name__ == "__main__":
    collection_path = input("Enter collection DB output path: ")
    if re.search(r"(\.db)", collection_path, flags=re.IGNORECASE) is None:  # had to use a raw string to avoid esc char
        collection_path = re.sub("$", ".db", collection_path)

    oc_dump = None
    while (oc_dump := input("Dump osu!Collector collection? [y/n]: ").strip().lower()) not in {'y', 'n', ''}:
        print(f"Not a valid input: {oc_dump}")

    if oc_dump == 'y':
        osu_collector_dump(collection_path)

    else:
        htm_dump = None
        while (htm_dump := input("Use a HTML/HTM file instead of list.txt (y/n): ").strip().lower()) not in {'y', 'n', ''}:
            print(f"Not a valid input: {htm_dump}")

        if htm_dump == 'y':
            html_dump(collection_path)

        else:
            print("Using list.txt...")
            list_txt_dump(collection_path)