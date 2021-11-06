import subprocess
import os
import re
import osu_collector_dumper
import list_mapid_info_puller
import html_to_list

html_check = "0"
osu_collector_check = "0"

osu_collector_check = input("Dump osu!Collector collection? (y/n): ")

if re.search("(y|Y)", osu_collector_check) != None:
    collection_id = input("Enter collection ID or URL: ")

if  re.search("(n|N)", osu_collector_check) != None:
    html_check = input("Use a HTML/HTM file instead of list.txt (y/n): ")

    if re.search("(y|Y)", html_check) != None:
        html_path = input("Enter path to HTML/HTM file: ")

api_key = input("Enter API key: ")
collection_path = input("Enter collection DB output path: ")

if re.search("(y|Y)", osu_collector_check) != None:
    osu_collector_dumper.osu_collector_dump(collection_id)

if re.search("(y|Y)", html_check) != None:
    html_to_list.html_to_list(html_path)

if re.search("(.(d|D)(b|B))", collection_path) == None:
    collection_path = re.sub("$", ".db", collection_path)

if re.search("(y|Y)", html_check) == None and re.search("(y|Y)", osu_collector_check) == None:
    html_to_list.html_to_list("list.txt")
    
list_mapid_info_puller.id_to_db(api_key, collection_path)
