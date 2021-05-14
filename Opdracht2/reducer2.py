#!/usr/bin/env python
"""reducer.py"""
#code source: https://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
from datetime import datetime


import sys

current_word = None
current_count = 0
word = None

for line in sys.stdin:
    line = line.strip() # remove leading and trailing whitespace
    word, count = line.split('\t', 1) # parse the input we got from mapper2.py

    count = int(count) # convert count (currently a string) to int

    if current_word == word:
        current_count += count
    else:
        if current_word:
            print ('%s\t%s' % (current_word, current_count))
        current_count = count
        current_word = word

if current_word == word:
    print ('%s\t%s' % (current_word, current_count))
