
import re

class BibtexEntry:
    def __init__(self, entrytype, bibid, fields):
        self.entrytype = entrytype
        self.bibid = bibid
        self.fields = fields

def find_char_after(string, char, index):
    for i in range(index, len(string)):
        if string[i]==char:
            return i
    raise IndexError("Can't find the char >"+char+"< in the string >"+string[index:]+"<")

def find_char_after_mirrorchar(string, target_char, index, open_char, close_char, espace_char="\\"):
    opened = 0
    if open_char==close_char:
        raise ValueError("target_char must not equal close_char")
    jump_next = False
    for i in range(index, len(string)):
        if jump_next:
            jump_next = False
            continue
        if string[i]==espace_char:
            jump_next = True
            continue
        if string[i]==open_char:
            opened += 1
            continue
        if string[i]==target_char:
            if opened==0:
                return i
        if string[i]==close_char:
            opened -= 1
    raise IndexError("Can't find the char >"+target_char+"< in the string >"+string[index:]+"<")

def contains_only_after(string, allowed, start, end_exclusive):
    for i in range(start, end_exclusive):
        if string[i] not in allowed:
            return False
    return True

def loads_entry(input):
    lastchar_index = input.rfind("}")
    start = 1
    end = find_char_after(input, "{", 1)
    entrytype = input[start:end]
    start = end+1
    end = find_char_after(input, ",", start)
    bibid = input[start:end]
    start = end+1
    fields = {}
    while True:
        if contains_only_after(input, " \t\n\r", start, lastchar_index):
            break
        end = find_char_after(input, "=", start)
        key = input[start:end].strip()
        start = find_char_after(input, "{", end)+1
        end = find_char_after_mirrorchar(input, "}", start, "{", "}")+1
        value = "{"+re.sub('[\t \n\r]+', ' ', input[start:end]).strip()
        start = end+1
        fields[key] = value
    return BibtexEntry(entrytype, bibid, fields)

def dumps_entry(bibtex_entry):
    output = "@"+bibtex_entry.entrytype+"{\n"
    l = []
    for key in bibtex_entry.fields.keys():
        l.append("  "+key+" = "+bibtex_entry.fields[key])
    output += ",\n".join(l)+"\n}"
    return output


def loads(input):
    start = 0
    output = []
    lastchar_index = input.rfind("}")
    while True:
        if contains_only_after(input, " \t\n\r", start, lastchar_index):
            break
        temp = find_char_after(input, "{", start)+1
        end = find_char_after_mirrorchar(input, "}", temp, "{", "}")+1
        output.append(loads_entry(input[start:end]))
        start = end
    return output