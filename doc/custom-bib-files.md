# How to add custom bib entries?
An entry for a publication may not be of type misc. It has to provide (entrytype, bibid and ) the following fields: ["personids", "author", "title", "year"].

- year is just the year eg `year = {2021}`
- title is the title of the publication eg `title = {The Example Title}`
- author is the author-string eg `author = {John Smith and Anna Carter}`
- personids is a hex formatted json-object. This is required because the author and editor fields do not provide enough information to uniquely identify the persons. The json object is a list. The list entries are dictionaries which must at least contain the field role and dblpid (orcid is optional). Valid roles are author and editor. **The entries must be in the same order as in the author and editor fields.** You can easily converted between the json object and hex using the hex2json.html in the html folder. eg `personids = {5b7b22726f6c65223a2022617574686f72222c202264626c706964223a20224a6f686e20536d697468227d2c7b22726f6c65223a2022656469746f72222c202264626c706964223a2022416e6e6120436172746572222c20226f72636964223a2022313233342d313233342d313233342d31323334227d5d}` which is hex for [{"role": "author", "dblpid": "John Smith 0001"},{"role": "editor", "dblpid": "Anna Carter", "orcid": "1234-1234-1234-1234"}]

*Important: Each entry must be covered by a misc entry in the criteria.bib file. The criteria.bib file holds all information about the venues and which publications belong to these venues. A publication is covered by a misc entry in the criteria.bib iff a prefix of the bibid of the publication is included in some misc entrys create-from field.*

* dblpid can be found on the dblp website. Search for the researcher, download as XML, and find the `<author>` Tag. the word between the opening and the closing tag is the dblpid
* orcid is a different unique id for researchers. They can be found in the `<author orcid="something">` tag. (It doesn't exist for every author in the dblp)

Example: 
bibid: custom:journals/jasis/RadhakrishnanV78
```
@misc{CRITERIA:DBLP:jasis,
    search-keys = {journals/jasis},
    create-from = {custom:journals/jasis},
    acronym = {JASIST},
    name = {Journal of the Association for Information Science and Technology}
}
```
or 
```
@misc{CRITERIA:DBLP:jasis,
    search-keys = {journals/jasis},
    create-from = {DBLP:journals/jasis, custom:journals/jasis},
    acronym = {JASIST},
    name = {Journal of the Association for Information Science and Technology}
}
```
Using the ir command you can do a sanity check on your custom bib file. `./ir-anthology-data custom check <custom-file>`
Keep in mind that this will not check for plausibility only the above mentioned requirements. 

Your custom bib file should be placed in the addidtional-bib-entries for future updates. You can add your custom bib file to the ir-anthology with `./ir-anthology-data custom add <custom-file>`
*Beware: This will overwrite any bib entries with the same bibid as the entries in your custom bib file.*

### commands

The commands can be installed via (from within `scripts/`)

```bash
python3 setup.py build
python3 setup.py install --user
```

Run the command from the repository root dir as `ir-anthology-data custom <check/add> <custom-file>`. It will add everything to `ir-anthology.bib`. Never add the same content twice to the same file.


### How to create author JSON

If you have the authors as a json string, it can be converted to hex in python by using `author_string.encode().hex()` where `encode()` converts a normal string `'<something>'` into a byte string `b'<something in bytes>'` and `hex()` converts it into the hex format.

Convert hex back to string by using `bytearray.fromhex(hex_string_as_normalstring).decode('utf-8')`.


### Other notes

* editors missing in `dir-2009.bib`
* The "dblpid"s for the following authors are dummys and don't actually exist in dblp: Tom Wuytack, Stephan Raajmakers, Inga Kohlhof, Toine Boggers, Hanna Jochmann-Mannak, Wouter Roelofs, Alessandro Tadeo Paula, Tristan Pothoven