#!/usr/bin/python

import string
import re
from os import system
import subprocess

# How strings are encoded
#	Turning off will remove all numbers in the code,
#	but will increase output size by a lot!
USE_HEXSTRINGS = False

# Remove comments from code
REMOVE_COMMENTS = True

# Obfuscate Python's built-in function calls
# 	Note: may make code large
OBFUSCATE_BUILTINS = True

# Force using no header variables
FORCE_NO_HEADER = False

# Special code replacements
REPLACEMENTS = {
	'True': '(()==())',
	'False': '(()==[])',
}

# Name of variable for internal actions (such as string decryption)
RESERVED_VAR = "__RSV"

RESERVED = [
	# Python reserved keywords
	'None', 'and', 'as', 'assert', 'break', 'class', 'continue',
	'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from',
	'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not',
	'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
]

# Python Built-in functions
# can be called like: getattr(__import__('builtins'), 'abs')(1)
BUILT_IN = [
	'abs', 'dict', 'help', 'min', 'setattr',
	'all', 'dir', 'hex', 'next', 'slice',
	'any', 'divmod', 'id', 'object', 'sorted',
	'ascii', 'enumerate', 'input', 'oct', 'staticmethod',
	'bin', 'eval', 'int', 'open', 'str',
	'bool', 'exec', 'isinstance', 'ord', 'sum',
	'bytearray', 'filter', 'issubclass', 'pow', 'super',
	'bytes', 'float', 'iter', 'print', 'tuple',
	'callable', 'format', 'len', 'property', 'type',
	'chr', 'frozenset', 'list', 'range', 'vars',
	'classmethod', 'getattr', 'locals', 'repr', 'zip',
	'compile', 'globals', 'map', 'reversed', '__import__',
	'complex', 'hasattr', 'max', 'round',
	'delattr', 'hash', 'memoryview', 'set'
]

# Might not be a complete list...
PREPAD = [';', ':', '=', '+', '-', '*', '%', '^', '<<', '>>', '|', '^', '/', ',', '{', '}', '[', ']']

number_variables = {}
variables = {}

# Header includes stuff like pre-processed integers
def getHeader():
	global number_variables
	global variables
	return ";".join("{}={}".format(number_variables[number], variables[number_variables[number]]) for number in sorted(number_variables, key = lambda x: len(number_variables[x]))) + "\n"

def addNumberToVars(number="", expression=""):
	global number_variables
	global variables
	
	if FORCE_NO_HEADER:
		return expression
	
	# 0 and 1 are used for number processing, so we should pre-process it before it is actually needed
	if ('0' not in number_variables) or ('1' not in number_variables):
		
		# Add 0 to the number variables
		variable_name = '_' * (len(variables) + 1)
		variables[variable_name] = '((()==[])+(()==[]))'
		#variables[variable_name] = '({0}^{0})'.format(number_variables['1'])
		number_variables['0'] = variable_name
		
		# Add 1 to the number variables
		variable_name = '_' * (len(variables) + 1)
		#variables[variable_name] = '((()==())+(()==[]))'
		variables[variable_name] = '({0}**{0})'.format(number_variables['0'])		# 1 = 0**0
		number_variables['1'] = variable_name
		
	if number == "":
		return
		
	if number in number_variables:
		return number_variables[number]
		
	# if the variable list is already too big,
	# it is better to just use the expression
	if len(expression) < (len(variables) + 1) + 2:
		return expression
		
	variable_name = '_' * (len(variables) + 1)
	variables[variable_name] = expression
	number_variables[number] = variable_name
	
	return variable_name
	

def encodeNumber(number):
	global number_variables
	global variables
		
	if int(number) < 0:
		#return "(~{}*{})".format(encodeNumber('0'), encodeNumber(abs(int(number))))		# Not working for some reason
		return "(({}-{})*{})".format(encodeNumber('0'), encodeNumber('1'), encodeNumber(-int(number)))
		
	number = str(number)
		
	if number in number_variables:
		return variables[number_variables[number]]
		
	# Try to avoid adding a header unless you really need to
	if number == '0':
		return '((()==[])+(()==[]))'
	elif number == '1':
		return '((()==())+(()==[]))'
		
	else:
		if ('0' not in number_variables) or ('1' not in number_variables):
			addNumberToVars()
		
		'''
		# Simpler way for smaller numbers
		if int(number) <= 4:
			expression = "({})".format("+".join([number_variables['1']] * int(number)))
			return expression
		'''
			
		# Convert a number to binary, then encode
		# eg.	13 	=> 1101 (binary)	=> (1 << 3)+(1 << 2)+(1 << 0)
		bin_number = bin(int(number))[2:]
		shifts = 0
		obf_number = ''
		while bin_number != '':
			if bin_number[-1] == '1':
				
				if str(1<<shifts) in number_variables:
					obf_number += number_variables[str(1<<shifts)]
					
				elif shifts >= 1:
					bit_m1 = addNumberToVars(str(1 << (shifts-1)), encodeNumber(str(1 << (shifts-1))))
					obf_number += '({}<<{})'.format(bit_m1, encodeNumber('1'))
				else:
					encode_bitshift = encodeNumber(str(shifts))
					obf_number += '({}<<{})'.format(number_variables['1'], encode_bitshift)
						
				obf_number += '+'
			
			bin_number = bin_number[:-1]
			shifts += 1
		obf_number = "({})".format(obf_number[:-1])
		return obf_number
		#return addNumberToVars(number, obf_number)
		
def encodeString(string):
	
	if USE_HEXSTRINGS:
		byte_array = "[{}]".format(",".join([hex(ord(c)) for c in string[1:-1]]))
	else:
		byte_array = "[{}]".format(",".join([encodeNumber(ord(c)) for c in string[1:-1]]))
	
	result = "''.join(chr({0}) for {0} in {1})".format(RESERVED_VAR, byte_array)
	return result
				

def obfuscate(code, append_header = True):
	global number_variables
	global variables
	
	global PREPAD
	global REPLACEMENTS
	
	# import statements should just be returned
	if code.split()[0] in ['import', 'from']:
		return code
		
	# Pad certain characters so they can be parsed properly
	prepadded = code
	for p in PREPAD:
		prepadded = prepadded.replace(p, " {} ".format(p))
	prepadded = prepadded.replace('(', "( ").replace(')', ' )')
	
	result = ''
	parsingQuote = ''
	lineCommented = False
	
	for symbol in prepadded.split():
		
		# Check if the rest of the line is commented
		if symbol[0] == '#':
			if REMOVE_COMMENTS:
				return
			lineCommented = True
			
		if lineCommented:
			result += symbol + ' '
			continue
		
		# If you encounter a string
		if (parsingQuote == '') and (symbol[0] in ["\"", "\'"]):
			parsingQuote = symbol + ' '
			continue
			'''
			if (symbol[0] == symbol[-1]) and (symbol != ''):
				result += encodeString(symbol)
				result += symbol
			else:
				parsingQuote = symbol + ' '
			continue
			'''
		
		if parsingQuote != '':
			if (symbol.find(parsingQuote[0]) != -1):
				parsingQuote += symbol[:symbol.find(parsingQuote[0])+1]
				result += encodeString(parsingQuote)
				parsingQuote = ''
			else:
				parsingQuote += symbol + ' '
			continue
			
			
		# Reserved words are passed along with spacing
		if symbol in RESERVED + BUILT_IN:
			result += " {} ".format(symbol)
			continue
		
		# arithmetic and similar symbols are passed along as well
		if symbol in PREPAD:
			result += symbol
			continue
		
		# special replacements
		if symbol in REPLACEMENTS:
			result += REPLACEMENTS[symbol]
			continue
		
		# Try to parse  it if it is an integer
		try:
			result += encodeNumber(int(symbol))
			continue
		except:
			pass			
		
		# Try to find the name of a variable / function
		name = ""
		for s in symbol:
			if s in string.ascii_letters + '_':
				name += s
			elif name not in variables:
				name = ""
		
		# If it is a variable/function, replace the old variable name with a new one
		if (name != "") and (name not in RESERVED) and (name not in BUILT_IN):
			if name not in variables:
				variables[name] = '_' * (len(variables) + 1)
			result += variables[name] + symbol[len(name):]
			continue
		
		# If there aren't any changes, just use the original code
		result += symbol
	
	# restore original indentation
	indents = ""
	i = 0
	while code[i] in ['\t', ' ']:
		indents += code[i]
		i += 1
	result = indents + result.strip()
	
	if append_header and (len(number_variables) > 0):
		return getHeader() + result
		
	return result
	
# For processing multiple lines at once
def obfuscate_lines(code):
	result = ""
	for line in code.split('\n'):
		if line:
			result += obfuscate(line, False) + "\n"
	return getHeader() + result


#encodeNumber('16')

#SAMPLE_CODE = 'x = 5'
#SAMPLE_CODE = 'for i in range(5): print([random.randrange(j+11) for j in range(13)]);'
#SAMPLE_CODE = 'print(sum(random.randrange(j+11) for j in range(7, 13)))'

#print(obfuscate(SAMPLE_CODE))
#print("The square root of " + str(n) + " is " + str(x))
# √
#print("The square root of " + str(n) + " = " + str(x))

# This example calculates the square root of n
SAMPLE_CODE = """
n = 17; x = 1
for i in range(100): x = x - ((x**2 - n) / (2*x))
print(x)
"""

with open('test.py', 'w') as fh:
	output = "".join(list(obfuscate_lines(SAMPLE_CODE)))
	fh.write(output)
	
	print('Written to test.py')

#
print('Output test run: \n')
subprocess.call('python test.py', shell=True)
	



'''
print("VARIABLES")
print(variables)
print()

print("OUTPUT")
print(output)

'''
#print()
#exec(output)