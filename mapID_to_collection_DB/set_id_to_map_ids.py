from typing import Any

from util import get_json_response

# TODO cache setID -> mapIDs as a local db to speed up lookups


# Writes all map IDs from set ID to list.txt
def set_id_list_to_map_id_list(set_ids: set, api_key) -> set:
    url = "https://osu.ppy.sh/api/get_beatmaps"
    ids = set()
    for set_id in set_ids:
        payload = {
            'k': api_key,
            's': set_id,
            'limit': 100,
        }

        beatmap_json: dict[str | Any] | None = None
        try:
            beatmap_json = get_json_response(url=url, payload=payload)
        except Exception as e:
            print("An exception occurred in set_id_list_to_map_id_list:\n"
                  f"{e}")

            # noinspection PyUnusedLocal
            user_input = None
            while (user_input := input(f"Create collection from {len(ids)} sets? (y/n)")) not in ('y', 'n'):
                print(f"Invalid input: {user_input}")

            if user_input == 'y':
                return ids

            else:
                quit(1)

        if beatmap_json is None:
            raise Exception("JSON response was received as None")

        beatmap_ids = []
        for beatmap in beatmap_json:
            beatmap_id = beatmap.get('beatmap_id')

            if beatmap_id is not None:
                beatmap_ids.append(beatmap_id)

            else:
                print(f"Beatmap set {set_id}: returned with an invalid id")  # TODO log this

        ids.add(*beatmap_ids)

        print(f"SetID - {set_id}:\n - {beatmap_ids}")  # TODO log this

    return ids
