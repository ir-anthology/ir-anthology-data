import click
from util import bibtexparser, rename as rn


@click.group(short_help='Change the bibib of bibtex entries .')
def rename():
    pass

@rename.command(short_help='Change the bibid of a single file. This is mainly for testing.')
@click.argument('input_file')
@click.argument('output_file')
def this(input_file, output_file):
    bibids = dict()
    with open(output_file, "w") as output_entries:
        with open(input_file, "r") as input_entries:
            for entry in bibtexparser.loads(input=input_entries.read()):
                if entry.bibid().startswith("CRITERIA:"):
                    output_entries.write(entry.string())
                    continue
                sourceid = entry.bibid()
                fields = entry.fields()
                new_bibid = rn.generate_bibid(sourceid, fields)
                if new_bibid not in bibids:
                    bibids[new_bibid] = 0
                else: 
                    bibids[new_bibid] += 1
                    new_bibid += "-"+str(bibids[new_bibid])
                string = rn.replace_bibid_add_source_id(entry.string(), sourceid, new_bibid)
                output_entries.write(string)





