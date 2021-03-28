from . import bibtexparser
import os
import wget
import gzip
from .util import find_char_after

def find_startindex_char(string, index, char):
    return find_char_after(string, char, index)

def startswith(string, start, prefix):
    if len(prefix)+start>len(string):
        return False
    for i in range(0, len(prefix)):
        if not string[start+i]==prefix[i]:
            return False
    return True



#iterative parser
dblp_topleveltags = ["article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www", "person", "data"]
def dblp_xml_iter_parser(gzfile):
    start = None
    end = None
    open_frame = False
    i = -1
    while True:
        i += 1
        if len(gzfile)<=i:
            break
        if not gzfile[i]=="<":
            continue
        for dblp_topleveltag in dblp_topleveltags:
            if not startswith(gzfile, i+1, dblp_topleveltag):
                continue
            if not open_frame:
                start = i
                open_frame = True
                break
            if open_frame:
                end = find_startindex_char(gzfile, i, ">")
                yield (start, end+1)
                i = end


def from_dblp(venuetype, acronym, year, issue):
    if not os.path.isdir(".cache/dblp"):
        os.makedirs(".cache/dblp/.raw")
        url = "https://dblp.uni-trier.de/xml/dblp.xml.gz"
        wget.download(url, '.cache/dblp/dblp.xml.gz')
        with gzip.open('.cache/dblp/dblp.xml.gz', 'rb') as gzfile:
            lines = []
            counter = 0
            xmls = ""
            last_tag = None
            open_frame = False
            for line in gzfile:
                line = line.decode("utf-8")
                while True:
                    match_index = None
                    if not open_frame:
                        for dblp_topleveltag in dblp_topleveltags:
                            match_index = line.find("<"+dblp_topleveltag)
                            if match_index == -1:
                                continue
                            last_tag = dblp_topleveltag
                            open_frame = True
                            break
                        if open_frame:
                            xmls = line[match_index:]
                        break                   
                    if open_frame:
                        match_index = line.find("</"+last_tag+">")
                        if match_index == -1:
                            xmls += line
                            break
                        match_index += len("</"+last_tag+">")
                        xmls += line[:match_index]
                        open_frame = False
                        quote_start = xmls.find(" key=\"")
                        quote_start += 6
                        quote_end = find_startindex_char(xmls, quote_start+1, "\"")
                        target_file_parts = xmls[quote_start:quote_end].split("/")
                        os.makedirs('.cache/dblp/'+"/".join(target_file_parts[0:1]), exist_ok=True)
                        target_file = '.cache/dblp/'+"/".join(target_file_parts[0:2])
                        with open(target_file, "a") as file:
                            counter+=1
                            if counter%10000==0:
                                print(counter)
                            #file.write(xmls)
                            #file.write("\n")


actionmap = {}
actionmap["--dblp"] = from_dblp


def main(args):
    venuetype = args[0]
    acronym = args[1]
    year = args[2]
    volume = "default"
    issue = None
    next_flag = 3
    if not args[3].startswith("--"):
        volume = args[3]
        next_flag += 1
        if not args[4].startswith("--"):
            issue = args[4]
            next_flag += 1
    if not args[next_flag].startswith("--"):
        raise Exception("asd")
    if args[next_flag] not in actionmap.keys():
        raise Exception("asd")
    actionmap[args[next_flag]](venuetype, acronym, year, issue)