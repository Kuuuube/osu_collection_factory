import re

def html_to_list(path_to_html):

    filepath = "list.txt"
    regex_finds_list = []
    
    with open (path_to_html, "r") as html_file:
        html_file_lines = html_file.readlines()
    html_list = list(map(str.strip, html_file_lines))
    
    for item in html_list:
        if re.search("^\d", item) == None:
            regex_filter_1 = re.findall("osu\.ppy\.sh/beatmaps/\d{1,8}", item)
            for regex_item in regex_filter_1:
                regex_filter_1_step_2 = re.findall("\d*$", regex_item)
                for regex_item in regex_filter_1_step_2:
                    if regex_item not in regex_finds_list:
                        regex_finds_list.append(regex_item)
            regex_filter_2 = re.findall("osu\.ppy\.sh/b/\d{1,8}", item)
            for regex_item in regex_filter_2:
                regex_filter_2_step_2 = re.findall("\d*$", regex_item)
                for regex_item in regex_filter_2_step_2:
                    if regex_item not in regex_finds_list:
                        regex_finds_list.append(regex_item)
            regex_filter_3 = re.findall("osu\.ppy\.sh/beatmapsets/\d{1,7}(#\w{1,6}/\d{1,8}|%23\w{1,6}/\d{1,8})", item)
            for regex_item in regex_filter_3:
                regex_filter_3_step_2 = re.findall("\d*$", regex_item)
                for regex_item in regex_filter_3_step_2:
                    if regex_item not in regex_finds_list:
                        regex_finds_list.append(regex_item)
            regex_filter_4 = re.findall("osu://b/\d{1,8}", item)
            for regex_item in regex_filter_4:
                regex_filter_4_step_2 = re.findall("\d*$", regex_item)
                for regex_item in regex_filter_4_step_2:
                    if regex_item not in regex_finds_list:
                        regex_finds_list.append(regex_item)
        else:
            mapid_check = re.findall("^\d*", item)
            for item in mapid_check:
                if item not in regex_finds_list:
                        regex_finds_list.append(item)
    with open (filepath, "w") as id_dump:
        for item in regex_finds_list:
            id_dump.writelines([item])
            id_dump.writelines(["\n"])
