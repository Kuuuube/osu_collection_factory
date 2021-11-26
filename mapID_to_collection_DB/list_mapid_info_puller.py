import json
import requests
import re
import time
import subprocess

def id_to_db(api_key, collection_path):

    collection_path_no_extension_1 = re.sub(".*(\\\|\\\\)", "", collection_path)
    collection_path_no_extension_2 = re.sub("\..*", "", collection_path_no_extension_1)
    filepath = 'CollectionCSVtoDB\\' + collection_path_no_extension_2 + '.csv'

    with open(filepath, 'w') as beatmap_info_file:
        beatmap_info_file.close()
    
    with open("list.txt", "r") as beatmapIDListRaw:
        	beatmapIDListLines = beatmapIDListRaw.readlines()
    beatmapIDList = list(map(str.strip, beatmapIDListLines))

    for element in beatmapIDList:
        beatmapid = element
        url = "https://osu.ppy.sh/api/get_beatmaps"
        payload = {
            'k': api_key,
            'b': beatmapid,
            'type': 'id',
            'limit': 100,
        }
        if len(beatmapid) > 0:
            r = requests.get(url, params=payload)
            beatmap = json.loads(r.text)
            beatmap_regex = re.search('(?<="file_md5": ").*?(?=")',json.dumps(beatmap))
            if beatmap_regex != None:
                print ("ID: " + beatmapid + " MD5: " + beatmap_regex.group(0))
    
                with open(filepath, 'a') as beatmap_info_file:
                    beatmap_info_file.writelines([",,"])
                    beatmap_info_file.writelines([beatmap_regex.group(0)])
                    beatmap_info_file.writelines(["\n"])

            time.sleep(1)
        if beatmapid == beatmapIDList[-1]:
            beatmap_info_file.close()
            subprocess.check_call([r"CollectionCSVtoDB\CollectionCSVtoDB.exe", filepath, collection_path])
            break
