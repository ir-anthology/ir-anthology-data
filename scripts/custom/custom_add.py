from custom import custom_check
import shutil
import click
from util import bibtexparser

def add(path_to_custom_bib, ignore_errors):
    if not ignore_errors:
        custom_check.check(path_to_custom_bib)
    else:
        try:
            custom_check.check(path_to_custom_bib)
        except Exception as e:
            print(e)
    with open(path_to_custom_bib, "r") as source:
        new_entries = bibtexparser.loads(source.read())
    d = {}
    for entry in new_entries:
        d[entry.bibid()] = entry
    with open(".cache/ir-anthology.bib", "w") as new_anthology:
        with open("ir-anthology.bib", "r") as anthology:
            for entry in bibtexparser.loads(anthology.read()):
                out = entry.string()
                if entry.bibid() in d:
                    out = d[entry.bibid()].string()
                    del d[entry.bibid()]
                print(out.strip(), file=new_anthology)
            for entry in d.values():
                print(entry.string().strip(), file=new_anthology)
    shutil.move(".cache/ir-anthology.bib", "./ir-anthology.bib")
