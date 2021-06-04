from util import bibtexparser

def main(path_main_bib, path_cache_bib, path_other_bib):
    with open(path_main_bib, "r") as main_bib:
        with open(path_cache_bib, "w") as cache_bib:
            with open(path_other_bib, "w") as other_bib:
                for entry in bibtexparser.loads(input=main_bib.read()):
                	bibid = entry.bibid()
                    if bibid.startswith("DBLP:"):
                        cache_bib.write(entry.string())
                        cache_bib.write("\n")
                    else:
                        if not bibid.startswith("CRITERIA:"):
                            other_bib.write(entry.string())
                            other_bib.write("\n")
    
