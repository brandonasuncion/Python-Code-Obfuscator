#!/usr/bin/env python3


#	Python Code Obfuscator
#	by Brandon Asuncion
#	
#	Questions/Comments?	me@brandonasuncion.tech


import string
import sys
import argparse

# How strings are encoded
#	Turning off will remove all numbers in the code,
#	but will increase output size by a lot!
USE_HEXSTRINGS = False

# Obfuscate Python's built-in function calls
OBFUSCATE_BUILTINS = False

# Remove comments from code
REMOVE_COMMENTS = True

# Special code replacements
REPLACEMENTS = {
	'True': '(()==())',
	'False': '(()==[])',
}

# Ignore the following two constants if you don't know what they mean
RESERVED_VAR = "__RSV"		# Name of variable for internal actions (such as string decryption)
BUILTINS_CONST = "__B"		# name used in the header for storing the "builtins" string

_RESERVED = [
	# Python reserved keywords
	'None', 'and', 'as', 'assert', 'break', 'class', 'continue',
	'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from',
	'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not',
	'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
]

# Python Built-in functions
# can be called like: getattr(__import__('builtins'), 'abs')(1)
_BUILT_IN = [
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
_PREPAD = [';', ':', '=', '+', '-', '*', '%', '^', '<<', '>>', '|', '^', '/', ',', '{', '}', '[', ']']

class Obfuscator(object):
	
	def __init__(self):
		self.header_variables = {}
		self.variables = {}

	# Header includes stuff like pre-processed integers
	def getHeader(self):
		return ";".join("{}={}".format(self.header_variables[number], self.variables[self.header_variables[number]]) for number in sorted(self.header_variables, key = lambda x: len(self.header_variables[x]))) + "\n"
		
	def getVariable(self, variableName):
		pass

	def addHeaderVar(self, varName, expression):
				
		if varName in self.header_variables:
			return self.header_variables[varName]
		
		# if the variable list is already too big,
		# it is better to just use the expression
		if len(expression) < (len(self.variables) + 1) + 2:
			return expression
		
		variable_name = '_' * (len(self.variables) + 1)
		self.variables[variable_name] = expression
		self.header_variables[varName] = variable_name
	
		return variable_name
	

	def encodeNumber(self, number, addToHeader = False):
		
		
		if int(number) < 0:
			return "(~([]==())*{})".format(self.encodeNumber(abs(int(number))))		# Not working for some reason
			#return "(({}-{})*{})".format(self.encodeNumber('0'), self.encodeNumber('1'), self.encodeNumber(-int(number)))
		
		number = str(number)
		
		if number in self.header_variables:
			return self.variables[self.header_variables[number]]
		
		
		if number == '0':
			return '((()==[])+(()==[]))'
		elif number == '1':
			return '((()==())+(()==[]))'
		
		else:
			# Try to avoid adding a header unless you really need to
			
			if ('0' not in self.header_variables):
				self.addHeaderVar('0', '((()==[])+(()==[]))')
				self.addHeaderVar('1', '({0}**{0})'.format(self.header_variables['0']))
			
			# Convert a number to binary, then encode
			# eg.	13 	=> 1101 (binary)	=> (1 << 3)+(1 << 2)+(1 << 0)
			bin_number = bin(int(number))[2:]
			shifts = 0
			obf_number = ''
			while bin_number != '':
				if bin_number[-1] == '1':
				
					if shifts == 0:
						obf_number += self.encodeNumber(1)
						
					elif str(1<<shifts) in self.header_variables:
						obf_number += self.header_variables[str(1<<shifts)]
					
					elif str(shifts) in self.header_variables:
						encode_bitshift = self.header_variables[str(shifts)]
						obf_number += '({}<<{})'.format(self.header_variables['1'], encode_bitshift)
						
					else:
						bit_m1 = self.encodeNumber(str(1 << (shifts-1)), True)
						obf_number += '({}<<{})'.format(bit_m1, self.encodeNumber('1'))
						
					obf_number += '+'
			
				bin_number = bin_number[:-1]
				shifts += 1
			if bin_number.count('1') == 1:
				obf_number = obf_number[:-1]
			else:
				obf_number = "({})".format(obf_number[:-1])
			
			if addToHeader:
				return self.addHeaderVar(number, obf_number)
			return obf_number
		
	def encodeString(self, string, addToHeader = False, forceHexstrings = False):
	
		if USE_HEXSTRINGS or forceHexstrings:
			#byte_array = "[{}]".format(",".join([hex(ord(c)) for c in string]))
			#result = "str(''.join(chr({0}) for {0} in {1}))".format(RESERVED_VAR, byte_array)
			result = "'{}'".format("".join("\\x{:02x}".format(ord(c)) for c in string))
		else:
			byte_array = "[{}]".format(",".join([self.encodeNumber(ord(c)) for c in string]))
			result = "str(''.join(chr({0}) for {0} in {1}))".format(RESERVED_VAR, byte_array)
		
		if addToHeader:
			return self.addHeaderVar(string, result)
		return result
				

	def obfuscate(self, code, append_header = True):
	
		# import statements should just be returned
		if code.split()[0] in ['import', 'from']:
			return code
		
		# Pad certain characters so they can be parsed properly
		prepadded = code
		for p in _PREPAD:
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
		
			# when it reaches the end of the string
			if parsingQuote != '':
				if (symbol.find(parsingQuote[0]) != -1):
					parsingQuote += symbol[:symbol.find(parsingQuote[0])+1]
					result += self.encodeString(parsingQuote[1:-1])
					parsingQuote = ''
				else:
					parsingQuote += symbol + ' '
				continue
			
			
			# Reserved words are passed along with spacing
			if symbol in _RESERVED:
				result += " {} ".format(symbol)
				continue
			
		
			# arithmetic and similar symbols are passed along as well
			if symbol in _PREPAD:
				result += symbol
				continue
		
			# special replacements
			if symbol in REPLACEMENTS:
				result += REPLACEMENTS[symbol]
				continue
		
			# if we find a number
			if symbol.isdigit():
				result += self.encodeNumber(int(symbol))
				continue
		
			# Try to find the name of a variable / function
			name = ""
			for s in symbol:
				if s in string.ascii_letters + '_':
					name += s
				elif name:
					#if name in self.variables
					if name[0] in string.digits:
						name = ""
					
			if name in _BUILT_IN:
				
				if OBFUSCATE_BUILTINS:
					if BUILTINS_CONST not in self.header_variables:
						self.addHeaderVar(BUILTINS_CONST, self.encodeString('builtins'))
					
					enc_name = self.addHeaderVar(name, self.encodeString(name))
					result += "getattr(__import__({}), {})".format(self.header_variables[BUILTINS_CONST], enc_name)
					result += symbol[len(name):]
				else:
					result += symbol
					
				continue
		
			# If it is a variable/function, replace the old variable name with a new one
			if (name != "") and (name not in _RESERVED) and (name not in _BUILT_IN):
				if name not in self.variables:
					self.variables[name] = '_' * (len(self.variables) + 1)
				result += self.variables[name] + symbol[len(name):]
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
	
		if append_header and (len(self.header_variables) > 0):
			return getHeader() + result
		
		return result
	
	# For processing multiple lines at once
	def obfuscate_lines(self, code):
		
		str_start = -1
		strings = []
		
		# get all strings in the code
		for i, c in enumerate(code):
			if (c in ['\'', '\"']) and (code[i-1] != '\\'):
				if str_start == -1:
					str_start = i
				elif c == code[str_start]:
					strings.append(code[str_start : i+1])
					str_start = -1
					
		# encode all the strings, and store them as variables in the header
		string_vars = {}
		for s in strings:
			encoded_str = self.encodeString(s[1:-1])
			string_vars[s] = self.addHeaderVar(s, encoded_str)
			
		for s in string_vars:
			code = code.replace(s, string_vars[s])
			
		
		result = ""
		for line in code.split('\n'):
			if not line:
				continue
			
			result += self.obfuscate(line, False) + "\n"
		return self.getHeader() + result
		
class MyArgParser(argparse.ArgumentParser):
	def error(self, message):
		sys.stderr.write('Error: {}\n'.format(message))
		self.print_help()
		sys.exit(2)

def main():
	parser = MyArgParser(description='Python Code Obfuscator by Brandon Asuncion (me@brandonasuncion.tech)')
	parser.add_argument('inputfile', help="Name of the input file")
	parser.add_argument('outputfile', help="Name of the output file")
	parser.add_argument('--debug', help="Show debug info", action="store_true")
	args = vars(parser.parse_args())
		
	print('Opening {} for obfuscation'.format(args['inputfile']))
	with open(args['inputfile'], 'r') as fh:
		lines = fh.read()
		
	obf = Obfuscator()
	output = obf.obfuscate_lines(lines)
		
	with open(args['outputfile'], 'w') as fh:
		fh.write(output)
		print('Written to {}\n'.format(args['outputfile']))
			
	if args['debug']:
		print('CONVERTED VARIABLES')
		for v in obf.variables:
			print("{}\t=> {}".format(v, obf.variables[v]))

		print('\nVARIABLES IN HEADER')
		for n in sorted(obf.header_variables, key=len):
			print("{}\t=> {}".format(n, obf.header_variables[n]))
		print()		

if __name__ == "__main__":
	main()
