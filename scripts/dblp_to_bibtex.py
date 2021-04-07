from util import bibtexparser
import xml.etree.ElementTree as ET
from queue import Queue
import re
from nameparser import HumanName
import html
import json
import os
from pylatexenc.latexencode import unicode_to_latex
from datetime import date



def iter_skip_first_last(iterator, first, last):
    iterator = iter(iterator)
    for _ in range(first):
        next(iterator)
    queue = Queue(maxsize = last+1)
    for item in iterator:
        queue.put(item)
        if queue.qsize()==last:
            break
    for item in iterator:
        queue.put(item)
        yield queue.get()

def authormap_to_bibtex_name(authormap):
    fullname = authormap["dblpid"]
    fullname = re.sub("\d", " ", fullname).strip()
    humanname = HumanName(fullname)
    firstname = humanname["first"] + " " + humanname["middle"]
    firstname = unicode_to_latex(firstname.strip())
    lastname = unicode_to_latex(humanname["last"])
    if firstname.find(" ")!=-1:
       firstname =  "{"+firstname+"}"
    if lastname.find(" ")!=-1:
        lastname = "{"+lastname+"}"
    return firstname + " " + lastname

dblp_venuetype_to_long_venuetype = {"conf": "conference", "journals":"journal"}
dblp_venuetype_venuename_to_real_venuename = {("journals", "www"): "WWWJ", ("journals", "sigir"): "SIGIR Forum"}

def split_venue_eventtype(input):
    venuetype, venue = input.split("/")[0:2]
    if (venuetype, venue) in dblp_venuetype_venuename_to_real_venuename:
        venue = dblp_venuetype_venuename_to_real_venuename[(venuetype, venue)]
    else:
        venue = venue.upper()
    venuetype = dblp_venuetype_to_long_venuetype[venuetype]
    return (venue, venuetype)


use_raw = set(["authors", "editors"])
forbidden_tags = set(["dblpkey", "metadata"])

def dblpid_to_bibid(dblpid):
    return "dblp/"+dblpid

def parse_xml(line):
    line = html.unescape(line).replace("&","&amp;")
    root = ET.fromstring(line)
    return root

def get_entrytype_bibid_fields(line):
    root = parse_xml(line)
    entrytype = root.tag
    bibid = dblpid_to_bibid(root.attrib["key"])
    fields = {}
    fields["metadata"] = {}
    fields["metadata"]["authors"] = []
    fields["metadata"]["editors"] = []
    fields["metadata"]["otherurls"] = []
    fields["venue"], fields["eventtype"] = split_venue_eventtype(root.attrib["key"])
    fields["dblpkey"] = root.attrib["key"]
    for item in list(root):
        if item.tag=="author" or item.tag=="editor":
            authormap = {}
            authormap["dblpid"] = item.text
            if "orcid" in item.attrib:
                authormap["orcid"] = item.attrib["orcid"]
            fields["metadata"][item.tag+"s"].append(authormap)
            continue
        if item.tag=="ee":
            ee = item.text
            if ee.endswith(".pdf"):
                fields["pdf"] = ee
                continue
            if ee.startswith("https://doi.org/"):
                fields["doi"] = ee[16:]
                continue
            if ee.startswith("http://doi.org/"):
                fields["doi"] = ee[15:]
                continue
            fields["metadata"]["otherurls"].append(ee)
            continue
        if item.tag=="url":
            fields["dblpurl"] = item.text
            continue
        if item.tag=="pages":
            fields["pages"] = item.text.replace("-", "--")
            continue
        if item.tag=="crossref":
            fields["crossref"] = "dblp/"+item.text
            continue
        if item.tag=="title":
            temp = "".join(list(item.itertext()))
            if temp.endswith("."):
                fields["title"] = temp[:-1]
            else:
                fields["title"] = temp
            continue
        if item.tag in forbidden_tags:
            raise Exception("Forbidden tag:"+item.tag)
        fields[item.tag] = item.text
    fields["authors"] = " and ".join(map(authormap_to_bibtex_name , fields["metadata"]["authors"]))
    fields["editors"] = " and ".join(map(authormap_to_bibtex_name , fields["metadata"]["editors"]))
    if fields["editors"] == "":
        del fields["editors"]
    if fields["authors"] == "":
        del fields["authors"]
    return (entrytype, bibid, fields)

def main1(array):
    if len(array)!=3:
        raise Exception("needes 3 arguments: dblp_selection_path, bibtex_folder, bibtex_file")
    main(array[0], array[1], array[2])

def extract_year(title):
    match = re.search(r"(^|[^\d])(\d{4})($|[^\d])", title)
    if match:
        year = re.search(r"(^|[^\d])(\d{4})($|[^\d])", title).group(2)
        intyear = int(year)
        if intyear<1900 or date.today().year<intyear:
            raise Exception("infered year ("+year+") is implausible for:"+title)
        return re.search(r"(^|[^\d])(\d{4})($|[^\d])", title).group(2)
    else:
        raise Exception("title does not contain venue year:"+title)

def main(dblp_selection_path, bibtex_folder, bibtex_file):
    os.makedirs(bibtex_folder, exist_ok=True)
    bidid_to_title_year = {}
    crossrefset = set()
    with open(dblp_selection_path, "r") as xml_file:
        for line in iter_skip_first_last(xml_file, 1, 1):
            root = parse_xml(line)
            for item in list(root):
                if "crossref"==item.tag:
                    crossrefset.add("dblp/"+"".join(list(item.itertext())))
                    break
    with open(dblp_selection_path, "r") as xml_file:
        key_set = set()
        for i in ["volume", "series", "isbn", "publisher", "editors"]:
            key_set.add(i)
        for line in iter_skip_first_last(xml_file, 1, 1):
            entrytype, bibid, fields = get_entrytype_bibid_fields(line)
            if bibid not in crossrefset:
                continue
            bidid_to_title_year[bibid] = {}
            for tag in fields:
                if "title"==tag:
                    title = fields["title"]
                    year = extract_year(title)
                    bidid_to_title_year[bibid]["title"] = title
                    bidid_to_title_year[bibid]["year"] = year
                    bidid_to_title_year[bibid]["is_workshop"] = title.lower().find("workshop")!=-1
                    continue
                if tag in key_set:
                    if tag=="editors":
                        bidid_to_title_year[bibid]["metadata"] = {"editors":fields["metadata"]["editors"]}
                    bidid_to_title_year[bibid][tag] = fields[tag]
    with open(bibtex_folder+"/"+bibtex_file, "w") as bib_file:
        with open(dblp_selection_path, "r") as xml_file:
            for line in iter_skip_first_last(xml_file, 1, 1):
                entrytype, bibid, fields = get_entrytype_bibid_fields(line)
                if bibid in bidid_to_title_year:
                    fields["eventyear"] = bidid_to_title_year[bibid]["year"]
                    if bidid_to_title_year[bibid]["is_workshop"]:
                        fields["eventtype"] = "workshop"
                if "crossref" in fields:
                    if fields["crossref"] in bidid_to_title_year:
                        if "metadata" in bidid_to_title_year[fields["crossref"]] and "editors" in bidid_to_title_year[fields["crossref"]]["metadata"]:
                            fields["metadata"]["editors"] = bidid_to_title_year[fields["crossref"]]["metadata"]["editors"]
                        fields["eventyear"] = bidid_to_title_year[fields["crossref"]]["year"]
                        fields["booktitle"] = bidid_to_title_year[fields["crossref"]]["title"]
                        if bidid_to_title_year[fields["crossref"]]["is_workshop"]:
                            fields["eventtype"] = "workshop"
                        for key in bidid_to_title_year[fields["crossref"]]:
                            if key=="title" or key=="year" or key=="is_workshop" or key=="metadata":
                                continue
                            if key in fields:
                                continue
                            fields[key] = bidid_to_title_year[fields["crossref"]][key]
                    else: 
                        print("Warning: Guessing eventyear for "+bibid)
                        fields["eventyear"] = fields["year"]
                fields["metadata"] = json.dumps(fields["metadata"])
                bib_file.write(bibtexparser.dumps_entry(bibtexparser.BibtexEntry(entrytype, bibid, fields), use_raw))
                bib_file.write("\n\n")
                #print(bibtexparser.dumps_entry(bibtexparser.BibtexEntry(entrytype, bibid, fields), use_raw))
                #input("Press Enter to continue...")
                    
                    
            
