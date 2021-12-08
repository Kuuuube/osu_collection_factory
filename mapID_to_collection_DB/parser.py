import re

from os import PathLike

from list_mapid_info_puller import id_to_db
from set_id_to_map_ids import set_id_list_to_map_id_list


def parse_file():
    path_to_file = input("Enter path of file to parse (Default - list.txt): ")  # TODO is there a way to validate this

    if path_to_file == "":
        path_to_file = "list.txt"

    api_key = input("Enter osu! API key: ")  # TODO is there a way to validate this
    # TODO pull api key from file [optionally]

    id_dict = _parse_ids(path_to_file)

    map_ids_set = set_id_list_to_map_id_list(set_ids=id_dict["set_ids"], api_key=api_key)

    if len(id_dict["map_ids"]) != 0:
        for m in id_dict["map_ids"]:
            map_ids_set.add(m)

    id_to_db(map_ids_set, api_key)


def _parse_ids(path_to_file: PathLike | str | None) -> dict[str, set]:
    map_ids = set()
    set_ids = set()
    map_ids_raw = set()

    with open (path_to_file, "r") as f:
        f_lines = f.readlines()
    content = list(map(str.strip, f_lines))
    
    # Regex pattern to pull osu.ppy.sh/s/* links
    pattern = re.compile(r'(((http.{0,4})?osu\.ppy\.sh/(?!u)\w{1,11}/((\d{1,8})?((#|%23)\w{1,5}/\d{1,8}|\w{1,7}\?b=\d{'
                         r'1,8}(&m=\d)?)|\d{1,8}))|(^\d{1,8}))')
    # Regex pattern to pull set IDs if no map ID is specified
    set_id_pattern = re.compile(r"(?!(?<=ets/)\d{1,7}(#|%23))((?<=ets/)\d{1,7})")
    # Regex pattern to pull map IDs
    map_id_pattern = re.compile(r"(?<!ets/)(?<!/s/)(?<=\w/)\d{1,8}")
    # Regex pattern for raw map IDs
    raw_map_id_pattern = re.compile(r"^\d{1,8}")
    
    for line in content:
        for link in pattern.finditer(line):
            set_id = re.findall(set_id_pattern, link.group(0))
        
            # Only append if set ID is found without map ID
            if len(set_id) == 1:
                set_ids.add(*set_id)
            else:
                map_id = re.findall(map_id_pattern, link.group(0))
                

                # Only append if map ID is found
                if len(map_id) == 1:
                    map_ids.add(*map_id)

                else:
                    map_id_raw = re.findall(raw_map_id_pattern, link.group(0))

                if len(map_id_raw) == 1:
                    map_ids_raw.add(*map_id_raw)

                else:
                    print(f"invalid link? : {link.group(0)}")
                
    return {"set_ids": set_ids, "map_ids": map_ids, "raw_mapids": map_ids_raw}
