import sys


def add_to_matrix(org_occmatrix, line ):
    org_occmatrix[line[0][0]][line[0][1]] += line[1]
    return  org_occmatrix

def percentage_matrix_converter(matrix):
    for i in 'abcdefghijklmnopqrstuvwxyz $':
        tot = sum(list(matrix[i].values()))
        for j in 'abcdefghijklmnopqrstuvwxyz $':
            if tot > 0 and matrix[i][j] > 0:
                matrix[i][j] = round((matrix[i][j] / tot) * 100, 1)
    return matrix

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    org_occmatrix = {first: {second: 0 for second in 'abcdefghijklmnopqrstuvwxyz $'} for first in'abcdefghijklmnopqrstuvwxyz $'}
    for characters in eval(line):
        org_occmatrix = add_to_matrix (org_occmatrix, characters)
    org_occmatrix = percentage_matrix_converter(org_occmatrix)
    print ('%s' % (org_occmatrix))