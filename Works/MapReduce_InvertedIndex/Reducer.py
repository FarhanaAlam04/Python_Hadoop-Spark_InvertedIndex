#!/usr/bin/python3
# Author: Farhana Alam
from sys import stdin
import re

current_word = None
word = None
current_doc = None
doc_count_dict = {} # dictionary to keep all document-count info
#doclist = ''

for line in stdin:
    #remove leading and trailing whitespace (including newlines)
    line = line.strip()
    #split into word and document name
    word, document = line.split('\t', 1)

    #while the word is the same, 
    if current_word == word:

        #checking if the document is also same or not
        if current_doc == document: #same document
            doc_count_dict[document]=doc_count_dict.get(document)+1

        else:
            current_doc = document
            doc_count_dict[document] = doc_count_dict.get(document,0)+1

    else:
    #otherwise we received a new word, so print the existing dict_info and start a new one

        if current_word:
            #Sorting the dictionary for sorted by count in descending and by document in ascending
            sorted_doc_count = sorted(doc_count_dict.items(), key = lambda x: (-x[1], x[0]))

            #stringifying the dictionary
            stringified_doc_count = ', '.join(f'{count} {document}'for document, count in sorted_doc_count)

            #printing the current word with documents & counts
            print(f"{current_word}\t{stringified_doc_count}")

        #updating current word, document and dictionary for the first new word
        current_word = word
        current_doc = document
        doc_count_dict = {document : 1}

# print the last word
if current_word == word:

   #Sorting the dictionary for sorted by count in descending and by document in ascending
   sorted_doc_count = sorted(doc_count_dict.items(), key = lambda x: (-x[1], x[0]))

   #stringifying the dictionary
   stringified_doc_count = ', '.join(f'{count} {document}'for document, count in sorted_doc_count)

   #printing the last word with documents & counts
   print(f"{current_word}\t{stringified_doc_count}")


