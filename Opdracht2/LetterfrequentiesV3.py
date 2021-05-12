import copy
import time
from functools import reduce
from operator import getitem
'''Code buddy: Quinn de Groot'''

def turn_lines_into_characters(lines):
    '''Step 3.1: replace any unvalid value with a invalid sign'''
    def remover(
            sentence=""):  # source: https://stackoverflow.com/questions/55902042/python-keep-only-alphanumeric-and-space-and-ignore-non-ascii/55902074
        valid_values = list("abcdefghijklmnopqrstuvwxyz ")
        sentence = sentence.lower()
        for item in sentence:
            if item not in valid_values:
                sentence = sentence.replace(item, "$")
        return sentence

    removed_sentence = remover(lines)
    '''Step 3.2: cut the characters and the next letter/value of it and place them in a list'''
    def sentence_cutter(removed_sentence = ""):
        cutted_sentence = [removed_sentence[i:i+2] for i in range(0, len(removed_sentence)-1)]
        return cutted_sentence
    cutted_sentence = sentence_cutter(removed_sentence)
    return cutted_sentence

def insert_characters_to_matrix(occmatrix, characterslist):
    try:
        for characters in characterslist: #this will be used for train data
            occmatrix[characters[0]][characters[1]] += 1
    except IndexError: #this will be used for test data
        occmatrix[characterslist[0]][characterslist[1]] += 1
    return occmatrix

def percentage_matrix_converter(matrix):
    for i in 'abcdefghijklmnopqrstuvwxyz $':
        tot = sum(list(matrix[i].values()))
        for j in 'abcdefghijklmnopqrstuvwxyz $':
            if tot > 0 and matrix[i][j] > 0:
                matrix[i][j] = round((matrix[i][j] / tot) * 100, 1)
    return matrix

def scoring(testmatrix, engmatrix, nlmatrix):
    enscore = 0
    nlscore = 0
    print(testmatrix)
    for i in 'abcdefghijklmnopqrstuvwxyz $':
        for j in 'abcdefghijklmnopqrstuvwxyz $':
            if testmatrix[i][j] != 0:
                endiff = abs(testmatrix[i][j]-engmatrix[i][j])
                nldiff = abs(testmatrix[i][j]-nlmatrix[i][j])
                if endiff>nldiff:
                    nlscore+=1
                else:
                    enscore+=1
    if nlscore>enscore:
        return 'en'
    else:
        return 'nl'

if __name__ == "__main__":
    '''Train Data:'''
    org_occmatrix = {first: {second: 0 for second in 'abcdefghijklmnopqrstuvwxyz $'} for first in'abcdefghijklmnopqrstuvwxyz $'}
    '''Eng:'''
    enmatrix = copy.deepcopy(org_occmatrix)
    alicefile = open('alice.txt', 'r')
    engLines1 = alicefile.readlines()
    engcharacters1 = map(turn_lines_into_characters, engLines1)
    enmatrix = reduce(insert_characters_to_matrix, engcharacters1, enmatrix)

    forestfile = open('forest.txt', 'r')
    engLines2 = forestfile.readlines()
    engcharacters2 = map(turn_lines_into_characters, engLines2)
    enmatrix = reduce(insert_characters_to_matrix, engcharacters2, enmatrix)

    engpercmatrix = map(percentage_matrix_converter, [enmatrix])
    for item in engpercmatrix:
        print("en:", item)

    '''Nl:'''
    nlmatrix = copy.deepcopy(org_occmatrix)
    oorlogfile = open('oorlogverhaal.txt', 'r')
    nlLines1 = oorlogfile.readlines()
    nlcharacters1 = map(turn_lines_into_characters, nlLines1)
    nlmatrix = reduce(insert_characters_to_matrix, nlcharacters1, nlmatrix)


    wijenonsezeltjefile = open('wijenonsezeltje.txt', 'r')
    nlLines2 = wijenonsezeltjefile.readlines()
    nlcharacters2 = map(turn_lines_into_characters, nlLines2)
    nlmatrix = reduce(insert_characters_to_matrix, nlcharacters2, nlmatrix)

    kabouterfile = open('kabouter.txt', 'r', encoding="utf8")
    nlLines3 = kabouterfile.readlines()
    nlcharacters3 = map(turn_lines_into_characters, nlLines3)
    nlmatrix = reduce(insert_characters_to_matrix, nlcharacters3, nlmatrix)

    nlpercmatrix = map(percentage_matrix_converter, [nlmatrix])
    for item in nlpercmatrix:
        print("nl:", item)



    '''Test Data:'''
    testdata = open('sentences.nl-en.txt', 'r', encoding="utf8")
    testlines = testdata.readlines()
    for testline in testlines:
        testmatrix = copy.deepcopy(org_occmatrix)
        testcharacters = turn_lines_into_characters (testline)
        testmatrix = reduce(insert_characters_to_matrix, testcharacters, testmatrix)
        testpercmatrix = map(percentage_matrix_converter, [testmatrix])
        scored = scoring(testpercmatrix, engpercmatrix, nlpercmatrix)
    print(scored)
    for item in testpercmatrix:
        print("test:", item)
    print(testline)

