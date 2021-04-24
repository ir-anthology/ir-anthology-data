#read cache, other, criteria and bundle

import shutil

def main(path_cache_bib, path_other_bib, path_criteria_bib, path_bundle_bib):
    with open(path_bundle_bib,"w") as bundle:
        pass 
    with open(path_bundle_bib,"wb") as bundle:
        for f in [path_cache_bib, path_other_bib, path_criteria_bib]:
            with open(f,'rb') as fd:
                shutil.copyfileobj(fd, bundle)