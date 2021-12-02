from util import bibtexparser, rename
import urllib3
import html
import xml.etree.ElementTree as ET
import time
import datetime
import hashlib
import os
import json

last_crawl_time = -1
time_between_crawls = 5

def crawl(bibid):
    global last_crawl_time
    while time.time() < last_crawl_time+time_between_crawls:
        time.sleep(round(last_crawl_time+time_between_crawls-time.time())+1)
    last_crawl_time = time.time()
    utc_time = datetime.datetime.utcnow()
    print(utc_time.strftime('%d.%m.%Y %H:%M:%S') + " crawling "+bibid)
    http = urllib3.PoolManager()
    r = http.request('GET', "https://dblp.org/rec/"+bibid+".bib?param=1")
    return r.data.decode()

def addchecksum(line, bibtex_entry):
    lines = bibtex_entry.split("\n")
    res = lines[0]
    res += "\n  xml-checksum = {"+checksum(line)+"},\n"
    res += "\n".join(lines[1:])
    return res

def addpersonids_and_crossref(root, bibtex_entry):
    lines = bibtex_entry.split("\n")
    res = lines[0]
    personids = []
    crossref = None
    for item in list(root):
        if item.tag == "crossref":
            crossref = item.text
        if not item.tag=="author" and not item.tag=="editor":
            continue
        if item.tag=="author":
            authormap = {}
            authormap["role"] = "author"
            authormap["dblpid"] = item.text
            if "orcid" in item.attrib:
                authormap["orcid"] = item.attrib["orcid"]
        if item.tag=="editor":
            authormap = {}
            authormap["role"] = "editor"
            authormap["dblpid"] = item.text
            if "orcid" in item.attrib:
                authormap["orcid"] = item.attrib["orcid"]
        personids.append(authormap)
    res += "\n  personids = {" + json.dumps(personids).encode("UTF-8").hex() + "},\n"
    if crossref is not None:
        res += "  crossref = {" + "DBLP:"+crossref + "},\n"
    res += "\n".join(lines[1:])
    return res

def parse_xml(line):
    root = ET.fromstring(line)
    return root

def checksum(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def is_uptodate(cache, bibid, xmlentry):
    key = "DBLP:"+bibid
    if key not in cache:
        return False
    bib_checksum = cache[key].fields()["xml-checksum"]
    xml_checksum = checksum(xmlentry)
    return bib_checksum==xml_checksum

def main(path_cache_bib, path_selection_xmll):
    cache = {}
    with open(path_cache_bib, "r") as cache_bib:
        for entry in bibtexparser.loads(input=cache_bib.read()):
            cache[entry.fields()["sourceid"]] = entry
    with open(path_selection_xmll, "r") as xmll:
        with open(path_cache_bib+"2", "w") as cache_bib:
            for line in xmll:
                root = parse_xml(line)
                bibid = root.attrib["key"]
                entry_string = None
                if not is_uptodate(cache, bibid, line):
                    entry_string = addchecksum(line, crawl(bibid))
                    entry_string = addpersonids_and_crossref(root, entry_string)
                    fields = bibtexparser.load_fields(entry_string)
                    sourceid = "DBLP:"+bibid
                    new_bibid = rename.generate_bibid(sourceid, fields)
                    entry_string = rename.replace_bibid_add_source_id(entry_string, sourceid, new_bibid)
                else:
                    entry_string = cache["DBLP:"+bibid].string()
                cache_bib.write(entry_string)
    os.replace(path_cache_bib+"2", path_cache_bib)

def main1():  
    main("cache.bib", "selection.xmll")