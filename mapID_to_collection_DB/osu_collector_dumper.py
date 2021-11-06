import requests
import json
import re
import time
import sys

def osu_collector_dump(collection_id):

    collection_id_regex = re.search("\d*$", collection_id)
    
    hasMore = True
    cursor = "0"
    filepath = "list.txt"

    with open(filepath, 'w') as id_dump:
        id_dump.close()
    
    while hasMore == True:

        url = "https://osucollector.com/api/collections/" + collection_id_regex.group(0) + "/beatmapsv2?"
        payload = {
            "cursor": cursor,
            "perPage": "100"
        }

        r = requests.get(url, payload)
        collection = json.loads(r.text)
        
        print ("osu!Collectior: " + cursor + " waiting 5 seconds.")
        
        cursor = collection["nextPageCursor"]
        hasMore = collection["hasMore"]

        beatmap_list = (collection["beatmaps"])
        regex_filtered = re.findall('(?<="https://osu.ppy.sh/beatmaps/).*?(?=")', json.dumps(collection))

        for item in regex_filtered:
            with open (filepath, "a") as id_dump:
                id_dump.writelines([item])
                id_dump.writelines(["\n"])
            
        if hasMore == True:
            time.sleep(5)
