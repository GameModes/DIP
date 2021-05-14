import sys

def invalid_values_replacer(line):
    """
    :param line: a string line containing all values
    :return: a string line containing only valid values or a dollar sign
    """
    valid_values = list("abcdefghijklmnopqrstuvwxyz ")
    for item in line:
        if item not in valid_values:
            line = line.replace(item, "$") #replace non-valid values to dollar sign
    return line

# input comes from STDIN (standard input)
for line in sys.stdin:
    line = line.strip() # remove leading and trailing whitespace
    line = line.lower() # lower capitalized letters
    line = invalid_values_replacer(line)
    line = [line[item:item + 2]for item in range(len(line)-1)] #convert every character into a string + the next character
    line = map(lambda x: (x, 1), line) #add number 1 to every characters ('hi' -> ('hi', 1)) for easier use during counting
    print('%s\t' % (list(line)))


