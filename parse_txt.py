import re
import sys

def get_references(text):

    pattern = r"(\n[A-Z][a-z]+, +[A-Z]\. +[A-Z]*\.* *[A-Z]*\.*.*\(\d\d\d\d\)\..*?\n*?.*?\n*?.*?\n*?)(?=\n[A-Z][a-z]+, +[A-Z]\. +[A-Z]*\.* *[A-Z]*\.*)"

    match = re.findall(pattern, text)

    references = []

    for m in match:
        
        ref_split_newline = m.split('\n')
        
        ref_no_newline = ''
        for string in ref_split_newline:
            if string:
                ref_no_newline += string

        references.append(ref_no_newline)

    return references

def get_authors(reference):
    pattern = r"([A-Z][a-z]+, +[A-Z]\. +[A-Z]*\.* *[A-Z]*\.*)"
    match = re.findall(pattern, reference)

    authors = []

    for m in match:
        stripped = m.strip()
        authors.append(stripped)

    return authors

def get_year(reference):
    pattern = r"\((\d\d\d\d)\)"
    match = re.findall(pattern, reference)
    return match[0]

def get_title(reference):
    pattern = r"\(\d\d\d\d\). .*?\.?(.*?\.)"
    match = re.findall(pattern, reference)
    return match[0]

def main(argv):
    filename = argv

    # # possible solution to get the last ref
    # with open(filename, "a") as f:
    #     f.write("Cheng, K. M. C.")

    with open(filename) as f:
        text = f.read()

    references = get_references(text)

    for ref in references:
        print "------------------------"
        print "Authors: ", get_authors(ref)
        print "Year: ", get_year(ref)
        print "Title: ", get_title(ref)
        print "Full Reference: ", ref

if __name__=="__main__":
    main(sys.argv[1])