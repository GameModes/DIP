# Opdracht: Letterfrequenties
> Recognize Whether The Sentence Is English Or Dutch With An Accuracy Score Of At Least 90%

## Usage Command

OS X & Linux:

```sh
cat sentences.nl-en.txt | hadopy --mapper "python mapper.py" --reducer "python reducer.py" | hadopy --mapper "python mapper2.py" --reducer "python reducer2.py"
```

Windows:

```sh
type sentences.nl-en.txt | hadopy --mapper "python mapper.py" --reducer "python reducer.py" | hadopy --mapper "python mapper2.py" --reducer "python reducer2.
py"
```

## Usage example
To use it:
- Download the entire code as ZIP or clone it
- Put your text file in it (I use [test.txt](https://github.com/GameModes/DIP/blob/main/Opdracht2/test.txt))
- Use the Usage command For your OS system
  
This will give the amount of counted English and Dutch Sentences  
Since my test files was containing only english sentences this would be the output:  
![](smalltextOutput.png)

To really test out the code, lets use a bigger Text file.
[This Text File](https://github.com/GameModes/DIP/blob/main/Opdracht2/sentences.nl-en.txt) contains 73 Dutch and 119 Engels Sentences.
Running this will give the following output:  
![](bigtextOutput.png)  
It might not be correct, but it's accuracy is still higher than 90%.

## Library Install
Describe how to install all the Libraries

OS X & Linux:
```sh
pip3 install sys
pip3 install hadopy
```

Windows:
```sh
pip install sys
pip install hadopy
```

## Code Buddy
Quinn de Groot:
[https://github.com/DragonKiller952](github)


## Code Explaination
4 files are used in the following order:
mapper.py -> reducer.py -> mapper2.py -> reducer2.py
### mapper.py
- Reads text file with sys(.stdin)
- Splits it into sentences
- Replace the capitilized Letters with lower ones using the command .lower()
- Replace unvalid values (not in alfabet) with a dollar sign using the function: invalid_values_replacer()
- Split it into characters with holding the next character (love -> lo, ov, ve)
- Adding a number of the occurence of the characters (lo, ov, ve -> (lo, 1), (ov, 1), (ve, 1))
- Prints all the characters

### reducer.py
- Reads print from mapper.py with sys(.stdin) using the pipline
- Splits it into sentences
- Create an empty matrix containg all possible characters (it would look something like this: (a{a:0, b:0, c:0 etc..},b{a:0, b:0, c:0 etc..}, c{a:0, b:0, c:0 etc..}) )
- Add every character from mapper.py to the empty matrix using the function: add_to_matrix()
- Converts the entire matrix until percentages (a{a:2, b:5, c:3} -> a{a:20, b:50, c:30} so 20% change for aa)
- Prints this matrix

### mapper2.py
- As train data I have used 3 Dutch stories and 2 English Stories and convert them each into their own Matrix which are mentioned under the import
- Reads print from reducer.py with sys(.stdin) using the pipline
- Splits it into sentences
- While printed in reducer.py the matrix became a string so I convert to list again with eval()
- The nested for loop will calculate which matrix (eng or dutch) is closer to the testmatrix and the one with the lowest diff will give a string output "nl" or "en"
- And prints it

### reducer2.py (Used in wordcount assignment)
- Reads print from mapper2.py with sys(.stdin) using the pipline
- counts every output given by mapper2.py
- prints for every string given (in this case only "en" and "nl") the amount of occurences it has been given by mapper2.py

