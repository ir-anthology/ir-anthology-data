from .util import find_char_after
import os
import gzip

dblp_topleveltags = ["article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www", "person", "data"]

def find_startindex_char(string, index, char):
    return find_char_after(string, char, index)

def parse_selection_key_set(selection_list):
    return set(["conf/ecir"])

def main(dblp_path, selection_list, output_folder, output_filename):
    os.makedirs(output_folder, exist_ok=True)
    selection_key_set = parse_selection_key_set(selection_list)
    with open(output_folder+ "/" + output_filename, "w") as file:
        file.write("<dblpselection>\n")
        with gzip.open(dblp_path, 'rb') as gzfile:
            lines = []
            xmls = ""
            last_tag = None
            open_frame = False
            write_frame = False
            for line in gzfile:
                line = line.decode("utf-8")
                while True:
                    # some lines contain a close and an open tag
                    # which is why there is a while True here
                    match_index = None
                    if not open_frame:
                        for dblp_topleveltag in dblp_topleveltags:
                            match_index = line.find("<"+dblp_topleveltag)
                            if match_index == -1:
                                continue
                            last_tag = dblp_topleveltag
                            xmls = line[match_index:]
                            quote_start = xmls.find(" key=\"")
                            quote_start += 6
                            quote_end = quote_start+1
                            quote_end = find_startindex_char(xmls, quote_end, "/")+1
                            try:
                                quote_end = find_startindex_char(xmls, quote_end, "/")
                            except IndexError:
                                quote_end = find_startindex_char(xmls, quote_end, "\"")
                            key = xmls[quote_start:quote_end]
                            if key in selection_key_set:
                                write_frame = True
                            open_frame = True
                            break
                        break                   
                    if open_frame:
                        match_index = line.find("</"+last_tag+">")
                        if match_index == -1:
                            if write_frame:
                                xmls += line
                            break
                        open_frame = False
                        if write_frame:
                            match_index += len("</"+last_tag+">")
                            xmls += line[:match_index]
                            file.write(xmls.replace("\n",""))
                            file.write("\n")
                            write_frame = False
        file.write("</dblpselection>\n")

main("../.cache/dblp/dblp.xml.gz", None, "../.cache", "dblpselection.xml")