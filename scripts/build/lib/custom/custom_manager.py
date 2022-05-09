import click
from custom import custom_check
from custom import custom_add

@click.group(short_help='Manage custom bib entries.')
def custom():
    pass

@custom.command(short_help='Check custom bib entries.')
@click.argument('path_to_custom_bib')
def check(path_to_custom_bib):
    custom_check.check(path_to_custom_bib)

@custom.command(short_help='Add custom bib entries.')
@click.argument('path_to_custom_bib')
@click.option('--ignore-errors', help='Ignore the errors in the custom bib and add it anyways to the ir-athology. This action is highly discouraged. Please only use this flag if you exactly know what you are doing.', is_flag=True, default=False)
def add(path_to_custom_bib, ignore_errors):
    custom_add.add(path_to_custom_bib, ignore_errors)