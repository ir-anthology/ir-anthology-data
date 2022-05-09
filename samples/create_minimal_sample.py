'''This will create a minimal sample from the full ir-anthology.bib
* For every venue (per year) there will be at least 2 articles
* For every author, there will be at least 2 articles.
Since this will be created using the naive (greedy) solution, there will be frequently a couple more.'''

class Entry:
    def __init__(self):
        self.journal = None
        self.volume = None
        self.number = None
        self.publisher = None
        self.year = None

def index_of_close(text, open_symbol, close_symbol):
    stack = []
    flag = False
    for index, sign in enumerate(text):
        if sign==open_symbol:
            stack.append(True)
            flag = True
        elif sign==close_symbol:
            stack.pop()

        if flag and not stack: #stack == stack.isempty() for boolean comparisons
            return index

    return -1 #didn't close


def parse(entry_as_text):
    type_of_entry = entry_as_text[1:entry_as_text.index('{')]

    if type_of_entry == 'misc':
        return True #general information


    entry = Entry()

    content = entry_as_text[entry_as_text.index(',')+2:-1] #remove very last "}"

    while content:
        curranchor = content.index('=')
        key = content[1:curranchor].strip()
        curr_closes = index_of_close(content[curranchor:],'{','}')
        nextanchor = content.find('=',curranchor+curr_closes)
        valstart = content.index('{',curranchor+1)+1
        if nextanchor == -1: #no more afterwards
            value = content[valstart:content.rindex('}')]
            content = ''
        else:
            nextbegin = curranchor+curr_closes
            value = content[valstart:nextbegin]
            content = content[nextbegin+1:]
        value=value.strip()

        if key=='journal':
            entry.journal = value
        elif key=='volume':
            entry.volume = value
        elif key=='number':
            entry.number = value #keep as string, some have numbers "1-2"
        elif key=='publisher':
            entry.publisher = value
        elif key=='year':
            entry.year = value
            
                
    return entry


def keep(entry, covered):   
    if entry.journal:
        return entry.volume and entry.number and not (entry.journal in covered['journals'] and entry.volume in covered['journals'][entry.journal] and entry.number in covered['journals'][entry.journal][entry.volume] and covered['journals'][entry.journal][entry.volume][entry.number]>=2)
    elif entry.publisher:
        return entry.year and not (entry.publisher in covered['publishers'] and entry.year in covered['publishers'][entry.publisher] and covered['publishers'][entry.publisher][entry.year] >= 2)

def update(covered, entry):
    if entry.journal: #journal
        if not entry.journal in covered['journals']:
            covered['journals'][entry.journal] = {entry.volume: {entry.number:1}}
        elif not entry.volume in covered['journals'][entry.journal]:
            covered['journals'][entry.journal][entry.volume] = {entry.number:1}
        elif not entry.number in covered['journals'][entry.journal][entry.volume]:
            covered['journals'][entry.journal][entry.volume][entry.number] = 1

        else:
            covered['journals'][entry.journal][entry.volume][entry.number] += 1


    elif entry.publisher: #conference
        if not entry.publisher in covered['publishers']:
            covered['publishers'][entry.publisher] = {entry.year:1}
        elif not entry.year in covered['publishers'][entry.publisher]:
            covered['publishers'][entry.publisher][entry.year] = 1
        else:
            covered['publishers'][entry.publisher][entry.year] += 1


if __name__ == '__main__':
    SAMPLE_FILE = 'minimal-sample.bib'

    with open(SAMPLE_FILE, 'w') as sample: #create if nonexistent, override with empty content
        sample.write('')

    with open(SAMPLE_FILE,'a') as sample: #only appending
        with open('ir-anthology.bib','r') as bib:
            cached_entry = '' #string will contain whole entry
            covered = {'journals':{}, 'publishers':{}} #keep >=2 of each: venue, person, journal+volume+number (one each list page should be at least 2 papers)
            for line in bib: #this loads only current line -> not everything needs to be in the RAM
                #assume no new lines, entry after entry
                cached_entry += line
                if line == '}\n':
                    entry = parse(cached_entry)
                    keep_flag = False

                    if entry is True: # not an entry object
                        keep_flag = True

                    elif keep(entry, covered):
                        update(covered, entry)
                        keep_flag = True
 
                    if keep_flag:
                        sample.write(cached_entry)

                    cached_entry = '' # new entry starts


