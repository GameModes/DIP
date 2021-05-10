import copy
from deepdiff import DeepDiff
'''Step 1: create the big occurences dic'''
def occurenceslist_creator():
    alfabet = 'abcdefghijklmnopqrstuvwxyz $'
    occurenceslist = dict([(letter, []) for letter in alfabet]) #to create a dictionary with empty values with first letters as keys
    for firstletter in occurenceslist.keys():
        occurenceslist[firstletter].append(dict([(letter, 0) for letter in alfabet]))
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
      captilized_values = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
      for item in sentence:
        if item in captilized_values:
          sentence = sentence.replace(item, item.lower())
        elif item not in valid_values:
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
            first_character = cutted_characters[0]
            second_character = cutted_characters[1]
            matrixdic[first_character][0][second_character] += 1
        return matrixdic
    matrixdic = addto_occurences_dic(cutted_sentence, matrixdic)
    return matrixdic

'''Step 4: add every train data to their occurences matrixes'''
'''Step 4.1: retrieve traindata for English and Dutch'''
alicefile = open('alice.txt', 'r')
engLines1 = alicefile.readlines()
quicksandsfile = open('quicksands.txt', 'r')
engLines2 = quicksandsfile.readlines()

oorlogfile = open('oorlogverhaal.txt', 'r')
nlLines1 = oorlogfile.readlines()
wijenonsezeltjefile = open('wijenonsezeltje.txt', 'r')
nlLines2 = wijenonsezeltjefile.readlines()

'''Step 4.2: run every lines, make them valid and insert it into the matrix'''
for engLine1 in engLines1:
    engdic = add_sentence_to_matrix(engLine1, engdic)

for engLine2 in engLines2:
    engdic = add_sentence_to_matrix(engLine2, engdic)


for nlLine1 in nlLines1:
    nldic = add_sentence_to_matrix(nlLine1, nldic)

for nlLine2 in nlLines2:
    nldic = add_sentence_to_matrix(nlLine2, nldic)

'''Step 4.3: convert both matrixes to percentage'''
for i in 'abcdefghijklmnopqrstuvwxyz $':
        tot = sum(list(engdic[i][0].values()))
        for j in 'abcdefghijklmnopqrstuvwxyz $':
            if tot > 0 and engdic[i][0][j] > 0:
                engdic[i][0][j] = round((engdic[i][0][j]/tot)*100, 1)
print("English Percentage Occurences: ", engdic)

for i in 'abcdefghijklmnopqrstuvwxyz $':
        tot = sum(list(nldic[i][0].values()))
        for j in 'abcdefghijklmnopqrstuvwxyz $':
            if tot > 0 and nldic[i][0][j] > 0:
                nldic[i][0][j] = round((nldic[i][0][j]/tot)*100, 1)
print("Dutch Percentage Occurences: ", nldic)

'''Step 5: get the estimatations from the test data'''
'''Step 5.1: retrieve testdata for English and Dutch'''
testdata = open('../Opdracht2/sentences.nl-en.txt', 'r', encoding="utf8")
testlines = testdata.readlines()

'''Step 5.2: receive matrix'''
amount = 0
for testline in testlines:
    amount += 1
    testdatamatrix = copy.deepcopy(occurencesdic)
    testdatamatrix = add_sentence_to_matrix(testline, testdatamatrix)
    # print(testdatamatrix)

for i in 'abcdefghijklmnopqrstuvwxyz $':
        tot = sum(list(nldic[i][0].values()))
        for j in 'abcdefghijklmnopqrstuvwxyz $':
            if tot > 0 and nldic[i][0][j] > 0:
                testdatamatrix[i][0][j] = round((testdatamatrix[i][0][j]/tot)*100, 1)

print("Sentence ", amount, ": ", testline, "\n", testdatamatrix)
print(DeepDiff(testdatamatrix, nldic, significant_digits=1, ignore_string_case=True))