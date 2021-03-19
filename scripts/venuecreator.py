from . import bibtexparser
import os

def main(args):
    path = "data/"+args[0]+"/"+args[1]
    os.makedirs(path)
    entrytype = "misc"
    bibid = args[0]+"-"+args[1]+"-meta"
    fields = {}
    fields["name"] = "{"+args[2]+"}"
    if 4<=len(args):
        fields["description"] = "{"+args[3]+"}"
    with open(path+"/meta.bib", "w") as file:
        file.write(bibtexparser.dumps_entry(bibtexparser.BibtexEntry(entrytype, bibid, fields)))