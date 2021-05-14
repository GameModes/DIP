import sys

def invalid_values_replacer(line):
    valid_values = list("abcdefghijklmnopqrstuvwxyz ")
    for item in line:
        if item not in valid_values:
            line = line.replace(item, "$") #replace non-valid values to dollar sign
    return line

# input comes from STDIN (standard input)
for line in sys.stdin:
    line = line.strip() # split the line into words
    line = line.lower() # lower capitalized letters
    line = invalid_values_replacer(line)
    line = [line[item:item + 2]for item in range(len(line)-1)]
    line = map(lambda x: (x, 1), line)
    print('%s\t' % (list(line)))


