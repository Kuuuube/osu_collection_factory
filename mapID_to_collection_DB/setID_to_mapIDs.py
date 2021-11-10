import re
import json
import requests
import time

def setID_list_to_mapID_list(api_key):

    filepath = "list.txt"
    
    with open("setID_list.txt", "r") as setIDListRaw:
            	setIDListLines = setIDListRaw.readlines()
    setIDList = list(map(str.strip, setIDListLines))

    for element in setIDList:
            setid = element
            url = "https://osu.ppy.sh/api/get_beatmaps"
            payload = {
                'k': api_key,
                's': setid,
                'type': 'id',
                'limit': 100,
            }

            if len(setid) > 0:
                r = requests.get(url, params=payload)
                beatmap = json.loads(r.text)

                beatmap_regex = re.findall('(?<="beatmap_id": ").*?(?=")',json.dumps(beatmap))
                if beatmap_regex != None:
                    with open(filepath, 'a') as beatmap_info_file:
                        for item in beatmap_regex:
                            beatmap_info_file.writelines([item])
                            beatmap_info_file.writelines(["\n"])
                            print("SetID: " + setid + " MapID:" + item)
                time.sleep(1)
            if setid == setIDList[-1]:
                beatmap_info_file.close()
                break

def setID_to_list(path_to_setIDs):

    filepath = "setID_list.txt"
    duplicates_removed = []
    regex_finds_list = []
    
    with open (path_to_setIDs, "r") as setID_file:
        setID_file_lines = setID_file.readlines()
    SetID_list = list(map(str.strip, setID_file_lines))

    osu_strings = []
    for item in SetID_list:
        osu_strings.extend (re.findall("osu.ppy.sh/\w+/\d+.{0,3}\w{0,6}/{0,1}\d{0,8}", item))
        
    for item_string in osu_strings:
        if re.search("^\d", item_string) == None and re.search ("(#|%23)", item_string) == None:
            regex_filter_1 = re.findall("osu.ppy.sh/(beatmapsets/\d{1,7}(?<!#)|s/\d{1,7}(?<!#))", item_string)
            for regex_item in regex_filter_1:
                regex_filter_1_step_2 = re.findall("\d*$", regex_item)
                for regex_item_2 in regex_filter_1_step_2:
                    if regex_item_2 not in regex_finds_list:
                        regex_finds_list.append(regex_item_2)

    with open (filepath, "w") as id_dump:
        for dump_item in regex_finds_list:
            id_dump.writelines([dump_item])
            id_dump.writelines(["\n"])
