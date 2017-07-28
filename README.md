# Python Code Obfuscator
I was browsing /r/dailyprogrammer on Reddit one day, and attempted one of the daily challenges. After doing the challenge, I read through the comments and found a [very interesting submission](https://www.reddit.com/r/dailyprogrammer/comments/2ao99p/7142014_challenge_171_easy_hex_to_8x8_bitmap/cixkjuu/).

Seeing that baffled me at first sight, but after reading [/u/ntxhhf's breakdown](https://www.reddit.com/r/dailyprogrammer/comments/2ao99p/7142014_challenge_171_easy_hex_to_8x8_bitmap/ciza4c9/) of his code, I was inspired to make my own code obfuscator for Python using the ideas in his post.

*What exactly does this script do?*  
It takes your regular-looking Python code, and obfuscates it! It takes any specified Python script, and will attempt to create an equivalent script that has the *same exact* functionality as the original, but is incredibly difficult for humans to read regularly.

*So... how is this useful?*  
According to [Wikipedia](https://en.wikipedia.org/wiki/Obfuscation_(software))...
> Programmers may deliberately obfuscate code to conceal its purpose (security through obscurity) or its logic or implicit values embedded in it, primarily, in order to prevent tampering, deter reverse engineering, or even as a puzzle or recreational challenge for someone reading the source code.

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
__=((()==[])+(()==[]));___=(__**__);____=((___<<___));_____=((____<<(__**__)));______=((_____<<(__**__)));
_________=((___<<_____));__________=((((___<<_____))<<(__**__)));_=((__**__)+(______<<(__**__)));_______=(__**__)
for ________ in range((_____+(_________<<(__**__))+(__________<<(__**__)))):
    _______=_______-((_______**((___<<___))-_)/(((___<<___))*_______))
print(_______)
```

### Obfuscating Strings
There are two ways the parser can encrypt strings. The first way is with hex strings, and the other using the number encoding method above.

**Example Input:** `print("Hello World!")`

**Output**
```python
_=((()==[])+(()==[]));__=(_**_);___=((__<<__));____=((___<<(_**_)));_____=((__<<____));______=((_____<<(_**_)));
_______=str(''.join(chr(__RSV) for __RSV in [((____<<(_**_))+(______<<(_**_))),((_**_)+____+______+(((_____<<(_**_)))<<(_**_))),
(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),
((_**_)+___+____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),((_____<<(_**_))),((_**_)+___+____+_____+(((_____<<(_**_)))<<(_**_))),
((_**_)+___+____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(___+_____+______+(((_____<<(_**_)))<<(_**_))),
(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(____+______+(((_____<<(_**_)))<<(_**_))),((_**_)+______)]))
print(_______)
```

### Hiding Calls to Python's Built-In Functions
In Python, we can call a built-in function indirectly: `getattr(__import__('builtins'), 'abs')(5)`  
So to call a function, we just use the string-encoding method detailed above. It's definitely not space-efficient, but it works!

**Input:** `print(chr(65))`  

**Output:**
```python
_=((()==[])+(()==[]));__=(_**_);___=((__<<__));____=((___<<(_**_)));
_____=((____<<(_**_)));______=((_____<<(_**_)));_______=((((_____<<(_**_)))<<(_**_)));
________=str(''.join(chr(__RSV) for __RSV in [((__<<__)+(______<<(_**_))+(_______<<(_**_))),
((_**_)+____+______+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_))),
((_**_)+_____+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_))),(____+_____+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_))),
(____+______+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_))),((_**_)+_____+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_))),
(___+____+_____+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_))),((_**_)+___+______+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_)))]));
_________=str(''.join(chr(__RSV) for __RSV in [(______+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_))),
(___+______+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_))),((_**_)+_____+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_))),
(___+____+_____+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_))),(____+______+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_)))]));
__________=str(''.join(chr(__RSV) for __RSV in [((_**_)+___+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_))),
(_____+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_))),(___+______+_______+(((((_____<<(_**_)))<<(_**_)))<<(_**_)))]))
getattr(__import__(________), _________)(getattr(__import__(________), __________)(((_**_)+(((((_____<<(_**_)))<<(_**_)))<<(_**_)))))
```

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
* **Is there a license?**  
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/).

## Credits
* Brandon Asuncion - Code  
    Questions/Comments? Feel free to contact me at: **me@brandonasuncion.tech**
* [/u/ntxhhf](https://www.reddit.com/r/dailyprogrammer/comments/2ao99p/7142014_challenge_171_easy_hex_to_8x8_bitmap/ciza4c9/) - For the idea, and his breakdown of using lists/sets to create boolean values and integers
