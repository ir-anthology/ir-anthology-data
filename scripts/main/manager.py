#!/usr/bin/python3
import dblp.dblp_manager as dblp_manager
import click


@click.group()
def main():
    pass

main.add_command(dblp_manager.dblp)
#dblp_cache.main("all.bib", "cache.bib", "other.bib")
#dblp_download.main("/tmp/dblp.xml.tar.gz", "criteria.bib", "/tmp/selection.xmll")
#dblp_cache_update.main1()
#main(sys.argv[1:])