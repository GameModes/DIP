import sys
def add_to_matrix(org_occmatrix, line ):
    """
    adds the line to the original occurences matrix (org_occmatrix)
    :param org_occmatrix: the current matrix containing all the counted characters
    :param line: the characters that needs to be added to the matrix
    :return: the matrix with the line added to it
    """
    org_occmatrix[line[0][0]][line[0][1]] += line[1]
    return org_occmatrix

def percentage_matrix_converter(matrix):
    """
    converts all values in every key in the matrix to a percentage of chance to occur in a key
    E.G.: (a{a:2, b:5, c:3} -> a{a:20, b:50, c:30} so 20% change for aa)
    :param matrix: a matrix where the amount of occurences is for every key value
    :return: a matrix where the percentage change of occurences is for every character in every key value
    """
    for i in 'abcdefghijklmnopqrstuvwxyz $':
        tot = sum(list(matrix[i].values()))
        for j in 'abcdefghijklmnopqrstuvwxyz $':
            if tot > 0 and matrix[i][j] > 0:
                matrix[i][j] = round((matrix[i][j] / tot) * 100, 1)
    return matrix

for line in sys.stdin:
    line = line.strip() # remove leading and trailing whitespace
    # parse the input we got from mapper.py
    org_occmatrix = {first: {second: 0 for second in 'abcdefghijklmnopqrstuvwxyz $'} for first in'abcdefghijklmnopqrstuvwxyz $'}
    #Creates an empty matrix containing all possible characters (it would look something like this: (a{a:0, b:0, c:0 etc..},b{a:0, b:0, c:0 etc..}, c{a:0, b:0, c:0 etc..}) )
    for characters in eval(line):
        org_occmatrix = add_to_matrix (org_occmatrix, characters)
    org_occmatrix = percentage_matrix_converter(org_occmatrix)
    print ('%s' % (org_occmatrix))