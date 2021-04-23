from util.util import find_char_after
import os
import gzip
from util import bibtexparser
import wget
import click
import sys

dblp_topleveltags = ["article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www", "person", "data"]

def find_startindex_char(string, index, char):
    return find_char_after(string, char, index)

def parse_selection_key_set(path_criteria_bib):
    output = set([])
    with open(path_criteria_bib, "r") as criteria_bib:
        for entry in bibtexparser.loads(criteria_bib.read()):
            if not entry.bibid().startswith("DBLP:"):
                continue
            output.add(entry.fields()["search-key"])
    return output

def download():
    print("pulling the dblp.xml from https://dblp.uni-trier.de/xml/dblp.xml.gz")
    url = "https://dblp.uni-trier.de/xml/dblp.xml.gz"
    wget.download(url, path_dblp_xml)

def select(path_dblp_xml, path_criteria_bib, path_selection_output_xmll):
    print("one dot equals one million lines of the xml")
    selection_key_set = parse_selection_key_set(path_criteria_bib)
    with open(path_selection_output_xmll, "w") as file:
        with gzip.open(path_dblp_xml, 'rb') as gzfile:
            xmls = ""
            last_tag = None
            open_frame = False
            write_frame = False
            counter = 0
            for line in gzfile:
                if counter % 1000000 == 0:
                    print(".", end="")
                    sys.stdout.flush()
                counter += 1
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
