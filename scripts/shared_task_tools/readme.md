##extract_paper.py

extract_paper.py is a tool to split a proceedings PDF into it´s papers.

###how to use

python extract_paper.py pdfpath paperpath contentstart contentend   
pdfpath: path/to/the/pdf.pdf  
paperpath: dir/to/save/papers/in  
!!In case the proceeding is split only the content for this part!!  
contentstart: start of the content table -1  
contentend: end of the content table  
!!In case the proceeding is split only the content for this part!!  

for example:    
```python extract_paper.py goos21-overview-of-lilas-2021-living-labs-for-academic-search.pdf paper 17 21```

###wip

Currently there is no way to avoid the papers that are in front of new sections to have the new section-page at the end.  
Also the proceedings structure is inconsistent. F.e. ecir2021-1 has a link to the autor section ecir2021-2 doesnt.
This leads to the last paper not beeing extracted at the moment
##get_bib_keys.py

get_bib_keys.py is a tool to retrieve the bibkeys of papers.
It takes the proceeding, splits it into its papers and retrives their bibkeys from the IR-Anthologie.
It currently works for proceedings from ceur or trec.   
!!Some searches may not be unambiguous and the script will warn you if a Search doesn´t work!!

###how to use

python get_bib_keys.py origin proceeding_url year   
origin: trec or ceur
proceeding_url: link to the proceeding   
year: year of the proceeding   

for example:    
```python get_bib_keys.py trec https://trec.nist.gov/pubs/trec29/xref.html 2020```

###wip
More origins may be added.  

The Search-part may need to be expanded, if more edge cases of searches not working, because of special characters emerge.