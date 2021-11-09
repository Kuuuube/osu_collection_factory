import subprocess
import os
import re
import osu_collector_dumper
import list_mapid_info_puller
import html_to_list
import setID_to_mapIDs

html_check = "0"
osu_collector_check = "0"
diff_filter_min = "0"
diff_filter_max = "9999"

osu_collector_check = input("Dump osu!Collector collection? (y/n): ")

if re.search("(y|Y)", osu_collector_check) != None:
    collection_id = input("Enter collection ID or URL: ")
    diff_filter_check = input("Filter by star rating? (y/n): ")
    if  re.search("(y|Y)", diff_filter_check) != None:
        diff_filter_min = input("Minimum star rating: ")
        diff_filter_max = input("Maximum star rating: ")
        
if  re.search("(n|N)", osu_collector_check) != None:
    html_check = input("Use a HTML/HTM file instead of list.txt (y/n): ")

    if re.search("(y|Y)", html_check) != None:
        html_path = input("Enter path to HTML/HTM file: ")

collection_path = input("Enter collection DB output path: ")

if re.search("(y|Y)", osu_collector_check) != None:
    if re.search("(.(d|D)(b|B))", collection_path) == None:
        collection_path = re.sub("$", ".db", collection_path)
        if re.search("(y|Y)", diff_filter_check) != None:
            osu_collector_dumper.osu_collector_dump_diff(collection_id, collection_path, diff_filter_min, diff_filter_max)
        if re.search("(y|Y)", diff_filter_check) == None:
            osu_collector_dumper.osu_collector_dump(collection_id, collection_path)
if re.search("(y|Y)", html_check) != None:
    api_key = input("Enter API key: ")
    
    setID_to_mapIDs.setID_to_list(html_path)
    html_to_list.html_to_list(html_path)

    setID_to_mapIDs.setID_list_to_mapID_list(api_key)
    list_mapid_info_puller.id_to_db(api_key, collection_path)
    
if re.search("(.(d|D)(b|B))", collection_path) == None:
    collection_path = re.sub("$", ".db", collection_path)

if re.search("(y|Y)", html_check) == None and re.search("(y|Y)", osu_collector_check) == None:
    api_key = input("Enter API key: ")

    setID_to_mapIDs.setID_to_list("list.txt")
    html_to_list.html_to_list("list.txt")

    setID_to_mapIDs.setID_list_to_mapID_list(api_key)
    list_mapid_info_puller.id_to_db(api_key, collection_path)
