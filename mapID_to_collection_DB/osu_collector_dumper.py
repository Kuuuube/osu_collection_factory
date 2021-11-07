import requests
import json
import re
import time
import sys
import subprocess

def osu_collector_dump(collection_id, collection_path, diff_filter_min, diff_filter_max):
    
    collection_path_no_extension_1 = re.sub(".*(\\\|\\\\)", "", collection_path)
    collection_path_no_extension_2 = re.sub("\..*", "", collection_path_no_extension_1)
    
    collection_id_regex = re.search("\d*$", collection_id)
    
    hasMore = True
    cursor = "0"
    filepath = "list.txt"
    csv_filepath = 'CollectionCSVtoDB\\' + collection_path_no_extension_2 + '.csv'

    with open(filepath, 'w') as id_dump:
        id_dump.close()

    with open(csv_filepath, 'w') as id_dump:
        id_dump.close()
    
    while hasMore == True:

        url = "https://osucollector.com/api/collections/" + collection_id_regex.group(0) + "/beatmapsv2?"
        payload = {
            "cursor": cursor,
            "perPage": "100",
            "sortBy": "difficulty_rating",
            "filterMin": diff_filter_min,
            "filterMax": diff_filter_max
        }

        r = requests.get(url, payload)
        collection = json.loads(r.text)
        
        print ("osu!Collectior: waiting 5 seconds.")
        print (cursor)
        
        cursor = collection["nextPageCursor"]
        hasMore = collection["hasMore"]

        beatmap_list = (collection["beatmaps"])
        regex_filtered = re.findall('(?<="https://osu.ppy.sh/beatmaps/).*?(?=")', json.dumps(collection))

        hashes_regex_filtered = re.findall('(?<="checksum": ").{32}', json.dumps(collection))
        
        for item in regex_filtered:
            with open (filepath, "a") as id_dump:
                id_dump.writelines([item])
                id_dump.writelines(["\n"])

        for item in hashes_regex_filtered:
            with open (csv_filepath, "a") as hash_dump:
                    hash_dump.writelines([",,"])
                    hash_dump.writelines([item])
                    hash_dump.writelines(["\n"])
        
        if hasMore == True:
            time.sleep(5)
            
    subprocess.check_call([r"CollectionCSVtoDB\CollectionCSVtoDB.exe", csv_filepath, collection_path])
