import click
import os
import dblp.dblp_upgrade as dblp_upgrade
import dblp.dblp_cache as dblp_cache
import dblp.dblp_download as dblp_download
import dblp.dblp_combine as dblp_combine

#create cache folder
os.makedirs(".cache/dblp", exist_ok=True)
path_dblp = ".cache/dblp/dblp.tar.gz"
path_criteria = "criteria.bib"
path_references = ".cache/dblp/references.xmll"
path_data = "ir-anthology.bib"
path_dblp_cache = ".cache/dblp/dblp_cache"
path_other_cache = ".cache/dblp/dblp_other_cache"


@click.group(short_help='Manage bib entries originating from the dblp.')
def dblp():
    pass

@dblp.command(short_help='Update references (dblp.xml) and extract changed/new entries that match the criteria - this will not change the ir-anthology.bib')
@click.option('--skip-download', help='skips the download, only selects the xml entries based on the criteria', is_flag=True, default=False)
def update(skip_download):
    if not skip_download:
        dblp_download.download(path_dblp)
    dblp_download.select(path_dblp, path_criteria, path_references)

@dblp.command(short_help='Crawl all extracted entries and append them and their meta data to the ir-anthology.bib - This will replace outdated entries. Only changes entries crawled from the dblp. Crawling 0.2 entries per second. ')
def upgrade():
    if not os.path.isfile(path_references):
        print("no references found - you can try to run 'ir-anthology-data dblp update'")
        exit(1)
    dblp_cache.main(path_data, path_dblp_cache, path_other_cache)
    dblp_upgrade.main(path_dblp_cache, path_references)
    dblp_combine.main(path_dblp_cache, path_other_cache, path_criteria, path_data)
