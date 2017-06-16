# Python Code Obfuscator
I was browsing /r/dailyprogrammer on Reddit one day, and attempted one of the [daily challenges](https://www.reddit.com/r/dailyprogrammer/comments/2ao99p/7142014_challenge_171_easy_hex_to_8x8_bitmap/). After doing the challenge, I read through the comments and found a [ very interesting submission](https://www.reddit.com/r/dailyprogrammer/comments/2ao99p/7142014_challenge_171_easy_hex_to_8x8_bitmap/cixkjuu/).

Seeing that baffled me at first sight, but after reading [/u/ntxhhf's breakdown](https://www.reddit.com/r/dailyprogrammer/comments/2ao99p/7142014_challenge_171_easy_hex_to_8x8_bitmap/ciza4c9/) of his code, I was inspired to make my own code obfuscator for Python using the ideas in his post.

## Usage
``` $ python obfuscator.py inputfile outputfile
```

## Examples

### Hiding Numerical Values
Using Netwon's Method to find the square root of 17:
```n = 17; x = 1
for i in range(100): x = x - ((x**2 - n) / (2*x))
print(x)
```
Output
```__=((()==[])+(()==[]));___=(__**__);____=((___<<___));_____=((____<<(__**__)));______=((_____<<(__**__)));_________=((___<<_____));__________=((((___<<_____))<<(__**__)))
_=((__**__)+(______<<(__**__)));_______=(__**__)
for ________ in range((_____+(_________<<(__**__))+(__________<<(__**__)))):_______=_______-((_______**((___<<___))-_)/(((___<<___))*_______))
print(_______)
```

### Obfuscating Strings
There are two ways the parser can encrypt strings. The first way is with hex strings, and the other using the number encoding method above.

Input:
``` print("Hello World!")
```

Hex Strings:
```_='\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64\x21'
print('\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64\x21')
```
With Number Encoding:
```_=((()==[])+(()==[]));__=(_**_);___=((__<<__));____=((___<<(_**_)));_____=((__<<____));______=((_____<<(_**_)));_______=str(''.join(chr(__RSV) for __RSV in [((____<<(_**_))+(______<<(_**_))),((_**_)+____+______+(((_____<<(_**_)))<<(_**_))),(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),((_**_)+___+____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),((_____<<(_**_))),((_**_)+___+____+_____+(((_____<<(_**_)))<<(_**_))),((_**_)+___+____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(___+_____+______+(((_____<<(_**_)))<<(_**_))),(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(____+______+(((_____<<(_**_)))<<(_**_))),((_**_)+______)]))
print(str(''.join(chr(__RSV) for __RSV in [((____<<(_**_))+(______<<(_**_))),((_**_)+____+______+(((_____<<(_**_)))<<(_**_))),(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),((_**_)+___+____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),((_____<<(_**_))),((_**_)+___+____+_____+(((_____<<(_**_)))<<(_**_))),((_**_)+___+____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(___+_____+______+(((_____<<(_**_)))<<(_**_))),(____+(((___<<(_**_)))<<(_**_))+______+(((_____<<(_**_)))<<(_**_))),(____+______+(((_____<<(_**_)))<<(_**_))),((_**_)+______)])))
```
**Note**: Encoding strings is not very efficient using this sort of algorithm, but it works!

### Hiding Calls to Python's Built-In Functions
In Python, we can call a built-in function indirectly ```getattr(__import__('builtins'), 'abs')(5)```.
To call other functions, we would just use either of the two string encoding methods above.

Input:
```print(chr(65))
```
Output:
```_=str(''.join(chr(__RSV) for __RSV in [0x62,0x75,0x69,0x6c,0x74,0x69,0x6e,0x73]));__=str(''.join(chr(__RSV) for __RSV in [0x70,0x72,0x69,0x6e,0x74]));___=str(''.join(chr(__RSV) for __RSV in [0x63,0x68,0x72]));____=((()==[])+(()==[]));_____=(____**____);______=((_____<<_____));_______=((______<<(____**____)));________=((_______<<(____**____)));_________=((________<<(____**____)));__________=((_________<<(____**____)))
getattr(__import__(_), __)(getattr(__import__(_), ___)(((____**____)+(__________<<(____**____)))))
```

## Credits
* Brandon Asuncion (me@brandonasuncion.tech) - Code
* [/u/ntxhhf](https://www.reddit.com/r/dailyprogrammer/comments/2ao99p/7142014_challenge_171_easy_hex_to_8x8_bitmap/ciza4c9/) - For the idea, and his breakdown of using lists/sets to create boolean values and integers
