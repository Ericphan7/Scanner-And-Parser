

from enum import Enum
import re


class Token(Enum):

	###############
	# Token Table #
	###############

	# Format of members goes as follows:
	# TOKEN_MEMBER = ["lexeme matcher", numeric code]

	# Not Defined
	NOT_DEFINED = ["", 1]
	# Identifiers
	INTEGER_IDENTIFIER = ["", 2]
	FLOAT_IDENTIFIER = ["", 3]
	STRING_IDENTIFIER = ["", 4]
	BOOLEAN_IDENTIFIER = ["", 5]
	# Constant Identifiers
	CONSTANT_INTEGER_IDENTIFIER = ["", 6]
	CONSTANT_FLOAT_IDENTIFIER = ["", 7]
	CONSTANT_STRING_IDENTIFIER = ["", 8]
	CONSTANT_BOOLEAN_IDENTIFIER = ["", 9]
	# Literals
	INTEGER_LITERAL = ["^[-+]?[0-9]+$", 10]
	FLOAT_LITERAL = ["^[-+]?\\d+(\\.\\d+)?$", 11]
	STRING_LITERAL = ["\".*\"", 12]
	BOOLEAN_LITERAL = ["^mtrue|mfalse$", 13]
	# Array Identifiers
	# ARRAY_INTEGER_IDENTIFIER = ["", 14]
	# ARRAY_FLOAT_IDENTIFIER = ["", 15]
	# ARRAY_STRING_IDENTIFIER = ["", 16]
	# ARRAY_BOOLEAN_IDENTIFIER = ["", 17]
	# Operators
	ASSIGNMENT_OPERATOR = ["=", 18]
	LE_OPERATOR = ["<=", 19]
	LT_OPERATOR = ["<", 20]
	GE_OPERATOR = [">=", 21]
	GT_OPERATOR = [">", 22]
	EQ_OPERATOR = ["==", 23]
	NE_OPERATOR = ["~=", 24]
	ADD_OPERATOR = ["\\+", 25]
	SUB_OPERATOR = ["-", 26]
	MUL_OPERATOR = ["\\*", 27]
	DIV_OPERATOR = ["/", 28]
	# Other Identifiers
	IDENTIFIER = ["", 29]
	FUNCTION_IDENTIFIER = ["", 30]
	SYMBOL_IDENTIFIER = ["", 31]
	# LB = ["\\[", 32]
	# RB = ["\\]", 33]
	# Reserved Keywords
	# SPECIFICATIONS = ["specifications", 1001]
	SYMBOL = ["symbol", 1002]
	# FORWARD = ["forward", 1003]
	# REFERENCES = ["references", 1004]
	FUNCTION = ["function", 1005]
	# POINTER = ["pointer", 1006]
	# ARRAY = ["array|array\\[.*?\\]", 1007]
	TYPE = ["type", 1008]
	# STRUCT = ["struct", 1009]
	IMPORT = ["import", 1010]
	INPUT = ["input", 1011]
	# ENUM = ["enum", 1012]
	GLOBAL = ["global", 1013]
	DECLARATIONS = ["declarations", 1014]
	IMPLEMENTATIONS = ["implementations", 1015]
	MAIN = ["main", 1016]
	# PARAMETERS = ["parameters", 1017]
	CONSTANTS = ["constants", 1018]
	BEGIN = ["begin", 1019]
	END_FUN = ["endfun", 1020]
	# IF = ["if", 1021]
	# THEN = ["then", 1022]
	# ELSE = ["else", 1023]
	# ENDIF = ["endif", 1024]
	# REPEAT = ["repeat", 1025]
	# UNTIL = ["until", 1026]
	# END_REPEAT = ["endrepeat", 1027]
	DISPLAY = ["display", 1028]
	SET = ["set", 1029]
	RETURN = ["return", 1030]
	DEFINE = ["define", 1031]
	OF = ["of", 1032]
	VARIABLES = ["variables", 1033]
	# WHILE = ["while", 1034]
	# DO = ["do", 1035]
	# END_WHILE = ["endwhile", 1036]
	IS = ["is", 1037]
	EXIT = ["exit", 1038]
	# Data Types
	INTEGER = ["integer", 2001]
	FLOAT = ["float", 2002]
	STRING = ["string", 2003]
	BOOLEAN = ["tbool", 2004]
	MVOID = ["mvoid", 2005]

	# Returns: lexeme string
	def getLexeme(self):
		return self.value[0]

	# Returns: numeric code int
	def getNumCode(self):
		return self.value[1]

	# Returns: numeric code of token with corresponding regex match of "word"
	@staticmethod
	def findNumCode(word):
		for token in Token:
			tokenLexeme = token.getLexeme()
			if len(re.findall(tokenLexeme, word)) == 1:
				return token.getNumCode()
		return -1

	# Returns: Token object of token with corresponding regex match of "word"
	# If no regex match is found, then returns Token.NOT_DEFINED
	@staticmethod
	def findToken(word):
		for token in Token:
			tokenLexeme = token.getLexeme()
			if len(re.findall(tokenLexeme, word)) == 1:
				return token
		return Token.NOT_DEFINED
