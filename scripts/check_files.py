from pybtex.database.input import bibtex
import pybtex.errors
import biblib
from urllib.parse import unquote
import os
import bibtexparser
from tqdm import tqdm 

pybtex.errors.set_strict_mode(False)


def check_bib(bib_path, ceph_path):
    """This file checks all bib entries of the ir-anthology. It compares the doi entries with the pdf file names to see which bib entry has no pdf file in the ceph directory."""

    bibtex_file = open(bib_path, "r")
    bib_database = bibtexparser.load(bibtex_file
                                     
    found_txt = open("./found_pfs.txt", "a")
    not_found_txt = open("./not_found_pfs.txt", "a")
    no_doi=open("./no_doi.txt","a")

    """parser=bibtex.Parser()
    bib_data=parser.parse_file(bib_path)
    print(bib_data.entries.keys())"""

    for bib_name, bib_entry in tqdm(bib_database.entries_dict.items()):
        try:
            doi = bib_entry["doi"]
        except:
            print(bib_name+" has no doi")
            no_doi.write(bib_name+" "+str(bib_entry)+"\n")
            doi = "0/0"
        doi_url = unquote(doi)
        found = 0
        doi_parts = doi_url.split("/")
        doi_prefix = doi_parts[0]
        doi_suffix = doi_parts[1]

        for pdf in os.listdir(ceph_path + doi_prefix):
            pdf_url = unquote(pdf)

            if pdf_url == doi_url:
                # pdf exists
                found_txt.write(
                    "for " +
                    doi_url +
                    " exists" +
                    pdf +
                    " in " +
                    ceph_path +
                    doi_prefix)
                # rename with bib_name
                os.rename(ceph_path + doi_prefix + pdf, bib_name)
                found = 1

        if found == 0:
            # pdf not found
            # looking in subdirs for pdf

            alldirs = [dir[0] for dir in os.walk(ceph_path)]

            for direct in alldirs:
                for pdf in os.listdir(direct):
                    if pdf.endswith(".pdf"):

                        pdf_url = unquote(pdf)

                        if pdf_url == doi_url:
                            # pdf exists

                            found_txt.write(
                                "for " + doi_url + " exists" + pdf + " in " + direct)
                            os.rename(direct + pdf, bib_name)
                            # write to a file that found with path
                            # rename with bib_name
                            found = 1

                    if found == 0:
                        # pdf not found
                        # append to file with unfound pdfs
                        not_found_txt.write(
                            "for " + doi_url + " exists no pdf in ceph")

    bibtex_file.close()
    found_txt.close()
    not_found_txt.close()


if __name__ == "__main__":
    check_bib(
        "/home/jason/Dokumente/work/webis/ir-anthology/github/ir-anthology-data/ir-anthology.bib",
        "/home/jason/Dokumente/work/webis/ir-anthology/wlgc_test/wlgc/papers-by-doi/")
