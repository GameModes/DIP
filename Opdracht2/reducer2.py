#!/usr/bin/env python
"""reducer.py"""
#code source: https://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
from datetime import datetime
import sys

current_characters = None
current_count = 0
characters = None

for line in sys.stdin:
    line = line.strip() # remove leading and trailing whitespace
    characters, count = line.split('\t', 1) # parse the input we got from mapper2.py
    count = int(count) # convert count (currently a string) to int

    if current_characters == characters: #if word already found
        current_count += count #increase the counting of that word by one (1 -> 2)
    else:
        if current_word: #print the word out
            print ('%s\t%s' % (current_characters, current_count)) #with the amount of occurences
        current_count = count
        current_characters = characters

if current_characters == characters: #and of course print the last word
    print ('%s\t%s' % (current_characters, current_count))
