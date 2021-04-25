#read cache, other, criteria and bundle

import shutil

def main(path_cache_bib, path_other_bib, path_criteria_bib, path_bundle_bib):
    with open(path_bundle_bib,"w") as bundle:
        pass 
    with open(path_bundle_bib,"w") as bundle:
        for f in [path_cache_bib, path_other_bib, path_criteria_bib]:
            with open(f,'r') as fd:
                shutil.copyfileobj(fd, bundle)