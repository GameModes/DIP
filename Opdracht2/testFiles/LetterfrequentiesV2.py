import copy
import time
from functools import reduce
from operator import getitem
'''Code buddy: Quinn de Groot'''

start_time = time.time()
'''Step 1: create the big occurences dic'''
def occurenceslist_creator():
    occurenceslist = {first: {second: 0 for second in 'abcdefghijklmnopqrstuvwxyz $'} for first in 'abcdefghijklmnopqrstuvwxyz $'}
    return occurenceslist

occurencesdic = occurenceslist_creator()
print("Empty Dictionary:", occurencesdic)

'''Step 2: Split up in empty eng and nl train occurences dic matrix'''
engdic = copy.deepcopy(occurencesdic)
nldic = copy.deepcopy(occurencesdic)

'''Step 3: Create functions to add sentences to a matrix'''
def add_sentence_to_matrix(sentence, matrixdic):
    '''Step 3.1: replace any unvalid value with a invalid sign'''
    def remover(sentence =""): #source: https://stackoverflow.com/questions/55902042/python-keep-only-alphanumeric-and-space-and-ignore-non-ascii/55902074
      valid_values = list("abcdefghijklmnopqrstuvwxyz ")
      sentence = sentence.lower()
      for item in sentence:
        if item not in valid_values:
          sentence = sentence.replace(item, "$")
      return sentence
    removed_sentence = remover(sentence)

    '''Step 3.2: cut the characters and the next letter/value of it and place them in a list'''
    def sentence_cutter(removed_sentence = ""):
        cutted_sentence = [removed_sentence[i:i+2] for i in range(0, len(removed_sentence)-1)]
        return cutted_sentence
    cutted_sentence = sentence_cutter(removed_sentence)

    '''Step 3.3: Add the occurences of the cutted sentence to the big occurences dictionary'''
    def addto_occurences_dic(cutted_sentence, matrixdic):
        for cutted_characters in cutted_sentence:
            "Reduce method:"
            mapList = [cutted_characters[0], cutted_characters[1]]
            # nextvalue = matrixdic[cutted_characters[0]][cutted_characters[1]] + 1

            #set reduce                                                 get reduce
            reduce(getitem, mapList[:-1], matrixdic) [mapList[-1]] = reduce(getitem, mapList, matrixdic) + 1

            "Non reduce method:"
            # first_character = cutted_characters[0]
            # second_character = cutted_characters[1]
            # matrixdic[first_character][second_character] += 1

        return matrixdic

    matrixdic = addto_occurences_dic(cutted_sentence, matrixdic)
    return matrixdic

'''Step 4: add every train data to their occurences matrixes'''
'''Step 4.1: retrieve traindata for English and Dutch'''
alicefile = open('alice.txt', 'r')
engLines1 = alicefile.readlines()
forestfile = open('forest.txt', 'r')
engLines2 = forestfile.readlines()

oorlogfile = open('oorlogverhaal.txt', 'r')
nlLines1 = oorlogfile.readlines()
wijenonsezeltjefile = open('wijenonsezeltje.txt', 'r')
nlLines2 = wijenonsezeltjefile.readlines()
kabouterfile = open('kabouter.txt', 'r', encoding="utf8")
nlLines3 = kabouterfile.readlines()

'''Step 4.2: run every line, make them valid and insert it into the matrix'''
for engLine1 in engLines1:
    engdic = add_sentence_to_matrix(engLine1, engdic)

for engLine2 in engLines2:
    engdic = add_sentence_to_matrix(engLine2, engdic)

for nlLine1 in nlLines1:
    nldic = add_sentence_to_matrix(nlLine1, nldic)

for nlLine2 in nlLines2:
    nldic = add_sentence_to_matrix(nlLine2, nldic)

for nlLine3 in nlLines3:
    nldic = add_sentence_to_matrix(nlLine3, nldic)

'''Step 4.3: create percentage converter function'''
def percentage_matrix_converter(dictionary):
    for i in 'abcdefghijklmnopqrstuvwxyz $':
        tot = sum(list(dictionary[i].values()))
        for j in 'abcdefghijklmnopqrstuvwxyz $':
            if tot > 0 and dictionary[i][j] > 0:
                dictionary[i][j] = round((dictionary[i][j] / tot) * 100, 1)
    return dictionary

'''Step 4.4: convert both matrixes to percentage'''
engdic = percentage_matrix_converter(engdic)
print("English Percentage Occurences: ", engdic)

nldic = percentage_matrix_converter(nldic)
print("Dutch Percentage Occurences: ", nldic)

traindata_exectime = time.time() - start_time
'''Step 5: get the estimatations from the test data'''
'''Step 5.1: retrieve testdata for English and Dutch'''
testdata = open('sentences.nl-en.txt', 'r', encoding="utf8")
testlines = testdata.readlines()

'''Step 5.2: create score function'''
def scoring(testmatrix):
    enscore = 0
    nlscore = 0
    for i in 'abcdefghijklmnopqrstuvwxyz $':
        for j in 'abcdefghijklmnopqrstuvwxyz $':
            if testmatrix[i][j] != 0:
                endiff = abs(testmatrix[i][j]-engdic[i][j])
                nldiff = abs(testmatrix[i][j]-nldic[i][j])
                if endiff>nldiff:
                    nlscore+=1
                else:
                    enscore+=1
    if nlscore>enscore:
        return 'en'
    else:
        return 'nl'

'''Step 5.3: Loop through every testline and use scoring() to calculate which dictionary is closer'''
amount = 0
nlcount = 0
engcount = 0
for testline in testlines:

    amount += 1
    testdatamatrix = copy.deepcopy(occurencesdic)
    testdatamatrix = add_sentence_to_matrix(testline, testdatamatrix)
    for i in 'abcdefghijklmnopqrstuvwxyz $':
        tot = sum(list(nldic[i].values()))
        for j in 'abcdefghijklmnopqrstuvwxyz $':
            if tot > 0 and nldic[i][j] > 0:
                testdatamatrix[i][j] = round((testdatamatrix[i][j] / tot) * 100, 1)


    score = scoring(testdatamatrix)
    if score == "nl":
        nlcount += 1
    else:
        engcount += 1
    print("Sentence ", amount, ": '''", testline, "''' Estimated Language: ", score)

print("\nThis test data contains:\nNL sentences: ", nlcount, " ENG sentences: ", engcount)
print("Train Data Time:--- ",traindata_exectime, " seconds ---\nTest Data Time:--- ", (time.time() - start_time)-traindata_exectime," seconds ---\nTotal Time:--- ",(time.time() - start_time), "seconds ---")




