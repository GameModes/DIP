import re

'''Step 1: create the big occurences list'''
def occurenceslist_creator():
    alfabet = 'abcdefghijklmnopqrstuvwxyz $'
    occurenceslist = dict([(letter, []) for letter in alfabet]) #to create a dictionary with empty values with first letters as keys
    for firstletter in occurenceslist.keys():
        occurenceslist[firstletter].append(dict([(letter, 0) for letter in alfabet]))
    return occurenceslist

occurencesdic = occurenceslist_creator()
print("Empty Dictionary:", occurencesdic)

'''Step 2: open up the files needed as test values/sentences'''
#manual made test sentence:
sentence = "Appels rijpen* beHAlve het$ wormpje ''/?"

alicefile = open('alice.txt', 'r')
aliceLines = alicefile.readlines()

'''Step 3: replace any unvalid value with a invalid sign'''
def remover(sentence =""): #source: https://stackoverflow.com/questions/55902042/python-keep-only-alphanumeric-and-space-and-ignore-non-ascii/55902074
  valid_values = list("abcdefghijklmnopqrstuvwxyz ")
  captilized_values = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
  for item in sentence:
    if item in captilized_values:
      sentence = sentence.replace(item, item.lower())
    elif item not in valid_values:
      sentence = sentence.replace(item, "$")
  return sentence

'''Step 4: cut the characters and the next letter/value of it and place them in a list'''
def sentence_cutter(removed_sentence = ""):
    cutted_sentence = [removed_sentence[i:i+2] for i in range(0, len(removed_sentence)-1)]
    return cutted_sentence

'''Step 5: Add the occurences of the cutted sentence to the big occurences dictionary'''
def addto_occurences_dic(cutted_sentence):
    for cutted_characters in cutted_sentence:
        first_character = cutted_characters[0]
        second_character = cutted_characters[1]
        occurencesdic[first_character][0][second_character] += 1
    return occurencesdic


for aliceline in aliceLines:
    valid_sentence = remover(aliceline)
    cutted_sentence = sentence_cutter(valid_sentence)
    occurencesdic = addto_occurences_dic(cutted_sentence)
print("After Alice's Text: ", occurencesdic)

valid_sentence = remover(sentence)
cutted_sentence = sentence_cutter(valid_sentence)
occurencesdic = addto_occurences_dic(cutted_sentence)
print("After Manual Text: ", occurencesdic)
