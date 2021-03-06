#!/usr/bin/python3

flags = [
    "--ignore-warnings"
]
import re
import json
from util import bibtexparser
import click

def check(path_to_custom_bib):
    #check_regex(path_to_custom_bib)
    check_required_fields(path_to_custom_bib)
    check_misc_coverage(path_to_custom_bib)

def check_regex(path_to_custom_bib):
    with open(path_to_custom_bib, "r") as bib:
        text = bib.read()
    match = re.match("^(( |\n)*@[a-zA-Z:/]+\{[^,]+,(( |\n)*(-|[a-zA-Z])+ *= *\{(.|\n)*\},)*( |\n)*(-|[a-zA-Z])+ *= *\{(.|\n)*\}( |\n)*\}( |\n)*)+$", text)
    if match is None:
        raise Exception("regex does not match")
    print("end of regex_check")

def check_required_fields(path_to_custom_bib):
    with open(path_to_custom_bib, "r") as bib:
        text = bib.read()
    required_fields = [["personids"], ["title"], ["year"], ["author", "editor"]]
    for entry in bibtexparser.loads(text):
        keys = entry.fields().keys()
        for required_field in required_fields:
            if len(set(required_field) & set(keys))==0:
                raise Exception("at least one of these required fields must be added to '" + entry.bibid() + "': " + repr(required_field))
        s = bytes.fromhex(entry.fields()["personids"]).decode('utf-8')
        s = json.loads(s)

        names = []
        for person in s:
            if not all(['role','dblpid'] in person):
                raise Exception('role and dblpid must be present in personids of ' + str(person) + ' in the entry ' + entry.bibid())

            name = person['dblpid']
            parts = name.split(' ')
            if re.match('^[0-9]{4}$',parts[-1]) != None:
                parts = parts[:-1] #forget number
                name = ' '.join(parts)
            
        if 'and\n'.join(names) != entry['author']:
            raise Exception("Names don't fit in entry: " + entry.bibid())

    print("end of check_required_fields")
            
def check_misc_coverage(path_to_custom_bib):
    with open(path_to_custom_bib, "r") as bib:
        text = bib.read()
    required_fields = set(["personids", "author", "title", "year"])
    entries = bibtexparser.loads(text)
    bibids = list(filter(lambda x: not x=="misc", map(lambda x: x.bibid(), entries)))
    with open("./criteria.bib", "r") as bib:
        text = bib.read()
    entries = bibtexparser.loads(text)
    for entry in entries:
        if not entry.entrytype()=="misc":
            continue
        for create_from in entry.fields()["create-from"].split(","):
            create_from = create_from.strip()
            bibids = list(filter(lambda key: not key.startswith(create_from), bibids))
    if len(bibids)!=0:
        raise Exception("there are bib entries which are not covered by a misc entry in criteria.bib: "+str(bibids))
    print("end of check_misc_coverage")
