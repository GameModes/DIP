# Opdracht: Letterfrequenties
> Recognize Whether The Sentence Is English Or Dutch With An Accuracy Score Of At Least 90%

## Usage Command

OS X & Linux:

```sh
cat testtext.txt | hadopy --mapper "python mapper.py" --reducer "python reducer.py" | hadopy --mapper "python mapper2.py" --reducer "python reducer2.py"
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
pip install sys
pip install hadopy
```

Windows:
```sh
pip3 install sys
pip3 install hadopy
```

## Code Buddy
Quinn de Groot:
[https://github.com/DragonKiller952](github)


## Code Explaination
4 files are used in the following order:
mapper.py -> reducer.py -> mapper2.py -> reducer2.py
### mapper.py
- test

