from custom import custom_check
import shutil
import click
from util import bibtexparser, rename

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
    with open("criteria.bib", "r") as source:
        new_entries = new_entries + bibtexparser.loads(source.read())
    d = {}
    for entry in new_entries:
        d[entry.bibid()] = entry
    bibids = set([])
    with open(".cache/ir-anthology.bib", "w") as new_anthology:
        with open("ir-anthology.bib", "r") as anthology:
            for entry in bibtexparser.loads(anthology.read()):
                out = entry.string()
                bibid = entry.bibid()
                if bibid.startswith("CRITERIA:"):
                    if bibid in d:
                        continue
                else:
                    sourceid = entry.fields()["sourceid"]
                    if sourceid in d:
                        entry = d[sourceid]
                        bibid, out = new_bibid(entry, bibids) 
                        del d[sourceid]
                    bibids.add(bibid)
                print(out.strip(), file=new_anthology)
            for entry in d.values():
                out = entry.string()
                if not  entry.bibid().startswith("CRITERIA:"):
                    _, out = new_bibid(entry, bibids) 
                print(out.strip(), file=new_anthology)
    shutil.move(".cache/ir-anthology.bib", "./ir-anthology.bib")


def new_bibid(entry, bibids):
    out = entry.string()
    fields = entry.fields()
    new_bibid = rename.generate_bibid(entry.bibid(), fields)
    if new_bibid in bibids:
        i = 1
        while new_bibid+"-"+str(i) in bibids:
            i += 1
        new_bibid = new_bibid+"-"+str(i)
    out = rename.replace_bibid_add_source_id(out, entry.bibid(), new_bibid)
    bibid = new_bibid
    return (new_bibid, out)