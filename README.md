# ir-anthology-data
This repository contains the data for the ir-anthology and a command to manage the data.

`ir-anthology.bib` contains all bib entries together with some meta data for the build process. The meta data is stored in `@misc` bib entries.
`criteria.bib` contains search criteria for targets like the dlbp and also annotates meta data about the venues. Parts of this file are merged into the `ir-anthology.bib`.

# Requirements
- ubuntu-like-os
- python3 ≥ 3.8.5
- pip3
- make
- bash

# first steps
Run `make` and then update the reference list with `./ir-anthology-data dblp upgrade`.

# run the command
Run `./ir-anthology-data --help` to list all top level commands.

You can print all available subcommands of the `dblp` command with `./ir-anthology-data dblp --help`

# the dblp command
Before you run other dblp command, you should always run the `update` command first.
`./ir-anthology-data dblp update`
This will check for any new/changed entries in the dblp.

To add these new/changed entries to the ir-anthology.bib run `./ir-anthology-data dblp upgrade`.
