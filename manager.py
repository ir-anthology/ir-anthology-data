#!/usr/bin/python3
import sys
import scripts.venuecreator as venuecreator
import scripts.ingestor as ingestor
import scripts.dblp_to_bibtex as dblp_to_bibtex

argumentmapper = {}
argumentmapper["--new"] = venuecreator.main
argumentmapper["--ingest"] = ingestor.main
argumentmapper["--temp"] = dblp_to_bibtex.main1


def main(args):
    if args[0] not in argumentmapper.keys():
        raise Exception("asd")
    argumentmapper[args[0]](args[1:])
        

main(sys.argv[1:])