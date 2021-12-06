from util import get_json_response

# TODO cache setID -> mapIDs as a local db to speed up lookups


# Writes all map IDs from set ID to list.txt
def set_id_list_to_map_id_list(set_ids: set, api_key):
    file_path = "list.txt"

    url = "https://osu.ppy.sh/api/get_beatmaps"
    for set_id in set_ids:
        payload = {
            'k': api_key,
            's': set_id,
            'limit': 100,
        }

        beatmap_json = get_json_response(url=url, payload=payload)

        beatmap_ids = []
        for beatmap in beatmap_json:
            beatmap_id = beatmap.get('beatmap_id')

            if beatmap_id is not None:
                beatmap_ids.append(beatmap_id)

        # Write map IDs after getting theme
        with open(file_path, 'a') as beatmap_id_dump:
            for beatmap_id in beatmap_ids:
                beatmap_id_dump.write(beatmap_id + "\n")

            print(f"SetID - {set_id}:\n - {beatmap_ids}")  # TODO log this
