import nameparser
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import unicodedata

import nltk
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

def normalize_string(input_string):
    return unicodedata.normalize('NFKD', input_string).encode('ASCII', 'ignore').decode("ASCII").replace(" ", "-")

def generate_bibid(bibid, fields):
    parts = []
    first_author = None
    if "author" in fields: 
        first_author = fields["author"]
    else: 
        if "editor" in fields:
            first_author = fields["editor"]
    if first_author is not None:
        first_author = first_author.split(" and ")[0]
        last_name = nameparser.HumanName(first_author).last
        last_name = normalize_string(last_name)
        parts.append(last_name)
    if "year" in fields:
        parts.append(fields["year"])
    if "title" in fields:
        first_word = list(filter(lambda x: x not in stop_words, word_tokenize(fields["title"].lower())))
        if len(first_word)!=0:
            first_word = normalize_string(first_word[0])
            parts.append(first_word)
    if len(parts) == 0:
        raise KeyError("Neither author, editor, year or title present in "+bibid)
    new_bibid = "-".join(parts).lower()
    return new_bibid

def replace_bibid_add_source_id(string, bibid, new_bibid):
    string = string.replace(bibid, new_bibid)
    end_pos = string.find("{")+1
    start_pos = string.find(",\n")+2
    new_string = string[:end_pos] + new_bibid + ",\n  sourceid  = {" + bibid + "},\n" + string[start_pos:]
    return new_string