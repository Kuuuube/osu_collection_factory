import re

from os import PathLike


def parse_ids(path_to_file: PathLike | str) -> dict[str, set]:
    map_ids = set()
    set_ids = set()

    with open(path_to_file, 'r') as f:
        content = f.read()

    # Regex pattern to pull osu.ppy.sh/s/* links
    pattern = re.compile(r'((http.{0,4})?osu\.ppy\.sh/(?!u)\w{1,11}/((\d{1,8})?((#|%23)\w{1,5}/\d{1,8}|\w{1,7}\?b=\d{'
                         r'1,8}(&m=\d)?)|\d{1,8}))')
    # Regex pattern to pull set IDs if no map ID is specified
    set_id_pattern = re.compile(r"(?!(?<=ets/)\d{1,7}(#|%23))((?<=ets/)\d{1,7})")
    # Regex pattern to pull map IDs
    map_id_pattern = re.compile(r"(?<!ets/)(?<!/s/)(?<=\w/)\d{1,7}")

    for link in pattern.finditer(content):
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
                print(f"invalid link? : {link.group(0)}")

    return {"set_ids": set_ids, "map_ids": map_ids}
