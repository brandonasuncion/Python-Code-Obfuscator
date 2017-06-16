# Python Code Obfuscator
I was browsing /r/dailyprogrammer on Reddit one day, and attempted one of the daily challenges. After doing the challenge, I read through the comments and found a [very interesting submission](https://www.reddit.com/r/dailyprogrammer/comments/2ao99p/7142014_challenge_171_easy_hex_to_8x8_bitmap/cixkjuu/).

Seeing that baffled me at first sight, but after reading [/u/ntxhhf's breakdown](https://www.reddit.com/r/dailyprogrammer/comments/2ao99p/7142014_challenge_171_easy_hex_to_8x8_bitmap/ciza4c9/) of his code, I was inspired to make my own code obfuscator for Python using the ideas in his post.

*What exactly does this script do?*  
It takes your regular-looking Python code, and obfuscates it! It takes any specified Python script, and will attempt to create an equivalent script that has the *same exact* functionality as the original, but is incredibly difficult for humans to read regularly.

*"So... how is this useful?"*  
According to [Wikipedia](https://en.wikipedia.org/wiki/Obfuscation_(software))...
> Programmers may deliberately obfuscate code to conceal its purpose (security through obscurity) or its logic or implicit values embedded in it, primarily, in order to prevent tampering, deter reverse engineering, or even as a puzzle or recreational challenge for someone reading the source code.

## Usage
```
usage: obfuscator.py [-h] [--debug] inputfile outputfile

positional arguments:
  inputfile   Name of the input file
  outputfile  Name of the output file

optional arguments:
  -h, --help  show this help message and exit
  --debug     Show debug info
 ```

## Examples

### Masking Numerical Values

**Input:** Using Netwon's Method to find the square root of 17
```python
n = 17; x = 1
for i in range(100): x = x - ((x**2 - n) / (2*x))
print(x)
```
**Output:**
```python
__=((()==[])+(()==[]));___=(__**__);____=((___<<___));_____=((____<<(__**__)));______=((_____<<(__**__)));_________=((___<<_____));__________=((((___<<_____))<<(__**__)))
_=((__**__)+(______<<(__**__)));_______=(__**__)
for ________ in range((_____+(_________<<(__**__))+(__________<<(__**__)))):_______=_______-((_______**((___<<___))-_)/(((___<<___))*_______))
print(_______)
```

### Obfuscating Strings
There are two ways the parser can encrypt strings. The first way is with hex strings, and the other using the number encoding method above.

**Example Input:**
`print("Hello World!")`

#### Using Number Encoding:
Encoding strings is not very efficient using this sort of algorithm, but it works!
```python
_=((()==[])+(()==[]));__=(_**_);___=((__<<__));____=((___<<(_**_)));_____=((__<<____));______=((_____<<(_**_)));_______=str(''.join(chr(__RSV) for __RSV in [((____<<(_**_))+(______<<(_**_))),((_**_)+____+______+(((_____<<(_**_)))<<(_**_))),(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),((_**_)+___+____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),((_____<<(_**_))),((_**_)+___+____+_____+(((_____<<(_**_)))<<(_**_))),((_**_)+___+____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(___+_____+______+(((_____<<(_**_)))<<(_**_))),(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(____+______+(((_____<<(_**_)))<<(_**_))),((_**_)+______)]))
print(str(''.join(chr(__RSV) for __RSV in [((____<<(_**_))+(______<<(_**_))),((_**_)+____+______+(((_____<<(_**_)))<<(_**_))),(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),((_**_)+___+____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),((_____<<(_**_))),((_**_)+___+____+_____+(((_____<<(_**_)))<<(_**_))),((_**_)+___+____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(___+_____+______+(((_____<<(_**_)))<<(_**_))),(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(____+______+(((_____<<(_**_)))<<(_**_))),((_**_)+______)])))
```

#### Hex Strings:
```python
_='\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64\x21'
print('\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64\x21')
```

### Hiding Calls to Python's Built-In Functions
In Python, we can call a built-in function indirectly `getattr(__import__('builtins'), 'abs')(5)`.
To call other functions, we would just use either of the two string encoding methods above.

**Input:**
```python
print(chr(65))
```

**Output:**
```python
_=str(''.join(chr(__RSV) for __RSV in [0x62,0x75,0x69,0x6c,0x74,0x69,0x6e,0x73]));__=str(''.join(chr(__RSV) for __RSV in [0x70,0x72,0x69,0x6e,0x74]));___=str(''.join(chr(__RSV) for __RSV in [0x63,0x68,0x72]));____=((()==[])+(()==[]));_____=(____**____);______=((_____<<_____));_______=((______<<(____**____)));________=((_______<<(____**____)));_________=((________<<(____**____)));__________=((_________<<(____**____)))
getattr(__import__(_), __)(getattr(__import__(_), ___)(((____**____)+(__________<<(____**____)))))
```

## Mini-FAQ
* **Should I use this for distributing my source code?**  
As of the time I'm writing this, I highly recommend against that idea. There are some instances of code in that the parser cannot handle (multi-line strings, for instance). Also, the output really won't do much to prevent reverse-engineering.
* **The output is too big! How do I reduce the output size?**  
As of right now, the biggest impact is the inefficiency of encoding strings. For the smallest output, make sure to set the following constants in the script:
   ```
   USE_HEXSTRINGS = True
   OBFUSCATE_BUILTINS = False
   REMOVE_COMMENTS = True
   ```
* **It's still too big!**  
That wasn't a question. But yes, I will be doing periodic optimizations to this project when I have time. After all, it is just a side-project for me! :)
* **Is there a license?**  
Yes, it is currently distributed under the [Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/).

## Credits
* Brandon Asuncion - Code  
    Questions/Comments? Feel free to contact me at: **me@brandonasuncion.tech**
* [/u/ntxhhf](https://www.reddit.com/r/dailyprogrammer/comments/2ao99p/7142014_challenge_171_easy_hex_to_8x8_bitmap/ciza4c9/) - For the idea, and his breakdown of using lists/sets to create boolean values and integers
