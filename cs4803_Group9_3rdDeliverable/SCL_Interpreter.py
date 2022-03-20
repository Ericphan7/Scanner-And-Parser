
from SCL_Parser import SCL_Parser
from NodeType import NodeType
from Token import Token
from Lexeme import Lexeme
import re


class SCL_Interpreter(SCL_Parser):

	# Constructor
	def __init__(self, sclFilePath):
		SCL_Parser.__init__(self, sclFilePath)
		self.globalVariables = {}
		self.globalConstants = {}
		self.implementVariables = {}
		self.implementConstants = {}

	# Performs Python-SCL Interpretation
	def interpret(self):
		print("Parsing SCL File", "\n")
		parseTree = super().parse()
		print("\nFinished Parsing SCL File")
		print("="*50, "\n")

		# Iterate through all of <program> node's direct children
		for node in parseTree.getRoot().getChildren():

			if node.getNodeType() is NodeType.IMPORT:
				# Nothing to interpret for imports in this subset of SCL
				pass

			elif node.getNodeType() is NodeType.SYMBOL:
				# Nothing to interpret for symbols in this subset of SCL
				pass

			elif node.getNodeType() is NodeType.GLOBALS:
				self.interpretGlobals(node)

			elif node.getNodeType() is NodeType.IMPLEMENT:
				self.interpretImplement(node)

	# Interprets globals
	def interpretGlobals(self, node):
		for child in node.getChildren():
			if child.getNodeType() is NodeType.CONST_DEC:
				self.interpretConstDec(child)
			elif child.getNodeType() is NodeType.VAR_DEC:
				self.interpretVarDec(child)

	# Interprets implement
	def interpretImplement(self, node):
		for child in node.getChildren():
			if child.getNodeType() is NodeType.FUNCT_LIST:
				self.interpretFunctList(child)

	# Interprets const_dec
	def interpretConstDec(self, node):
		# There should only be one child of <const_dec>
		for child in node.getChildren():
			if child.getNodeType() is NodeType.CONST_LIST:
				self.interpretConstList(child)

	# Interprets const_list
	def interpretConstList(self, node):
		for child in node.getChildren():
			if child.getNodeType() is NodeType.COMP_DECLARE:
				self.interpretCompDeclare(child)

	# Interprets var_dec
	def interpretVarDec(self, node):
		# There should only be one child of <var_dec>
		for child in node.getChildren():
			if child.getNodeType() is NodeType.VAR_LIST:
				self.interpretVarList(child)

	# Interprets var_list
	def interpretVarList(self, node):
		for child in node.getChildren():
			if child.getNodeType() is NodeType.COMP_DECLARE:
				self.interpretCompDeclare(child)

	# Interprets comp_declare
	def interpretCompDeclare(self, node):
		parent = node.getParent()
		greatGrandparent = parent.getParent().getParent()

		isConstant = True if parent.getNodeType() is NodeType.CONST_LIST else False
		isGlobal = True if greatGrandparent.getNodeType() is NodeType.GLOBALS else False

		lexemes = node.getScanLine().getLexemes()
		returnTypeToken = None

		for child in node.getChildren():
			if child.getNodeType() is NodeType.RET_TYPE:
				returnTypeToken = self.interpretRetType(child)

		if isGlobal is True:
			if isConstant is True:
				self.globalConstants[lexemes[1].getLexemeString()] = [lexemes[3].getLexemeString(), returnTypeToken]
			else:
				self.globalVariables[lexemes[1].getLexemeString()] = ["", returnTypeToken]
		else:
			if isConstant is True:
				self.implementConstants[lexemes[1].getLexemeString()] = [lexemes[3].getLexemeString(), returnTypeToken]
			else:
				self.implementVariables[lexemes[1].getLexemeString()] = ["", returnTypeToken]

	# Returns return type token
	def interpretRetType(self, node):
		lexemes = node.getScanLine().getLexemes()

		returnType = lexemes[len(lexemes)-1]
		returnTypeToken = returnType.getToken()

		return returnTypeToken

	# Interprets funct_list
	def interpretFunctList(self, node):
		for child in node.getChildren():
			if child.getNodeType() is NodeType.FUNCT_BODY:
				self.interpretFunctBody(child)

	# Interprets funct_body
	def interpretFunctBody(self, node):
		for child in node.getChildren():
			if child.getNodeType() is NodeType.CONST_DEC:
				self.interpretConstDec(child)
			elif child.getNodeType() is NodeType.VAR_DEC:
				self.interpretVarDec(child)
			elif child.getNodeType() is NodeType.PACTIONS:
				self.interpretPActions(child)

	# Interprets pactions
	def interpretPActions(self, node):
		for child in node.getChildren():
			if child.getNodeType() is NodeType.ACTION_DEF:
				self.interpretActionDef(child)

	# Interprets action_def
	def interpretActionDef(self, node):
		lexemes = node.getScanLine().getLexemes()

		# If action is to SET
		if lexemes[0].getToken() is Token.SET:
			if lexemes[1].getLexemeString() in self.globalVariables:
				expResult = None
				for child in node.getChildren():
					if child.getNodeType() is NodeType.EXP:
						expResult = self.interpretExp(child)
						self.globalVariables[lexemes[1].getLexemeString()][0] = expResult
			elif lexemes[1].getLexemeString() in self.implementVariables:
				expResult = None
				for child in node.getChildren():
					if child.getNodeType() is NodeType.EXP:
						expResult = self.interpretExp(child)
						self.implementVariables[lexemes[1].getLexemeString()][0] = expResult
			elif lexemes[1].getLexemeString() in (self.globalConstants, self.implementConstants):
				print("ERROR: Constant variable cannot be changed!")
			else:
				print("ERROR: Variable not found!")

		# If action is to INPUT
		elif lexemes[0].getToken() is Token.INPUT:
			if lexemes[1].getToken() is Token.STRING_LITERAL:
				if self.getVarType(lexemes[2].getLexemeString()) is not None:
					if lexemes[2].getLexemeString() in self.globalVariables:
						self.globalVariables[lexemes[2].getLexemeString()][0] = input(self.getStringLiteralTxt(lexemes[1].getLexemeString()))
					elif lexemes[2].getLexemeString() in self.implementVariables:
						self.implementVariables[lexemes[2].getLexemeString()][0] = input(self.getStringLiteralTxt(lexemes[1].getLexemeString()))
					elif lexemes[2].getLexemeString() in (self.globalConstants, self.implementConstants):
						print("ERROR: Constant Variable cannot be changed!")
					else:
						print("ERROR: Variable not found!")

		# If action is to DISPLAY
		elif lexemes[0].getToken() is Token.DISPLAY:
			# Should only be one child
			for child in node.getChildren():
				valueListTxt = self.interpretPVarValueList((child))
				print(valueListTxt)

	# Interprets p_var_value_list and returns a list of values
	def interpretPVarValueList(self, node):
		allLexemesOnLine = node.getScanLine().getLexemes()

		valueListLexemes = allLexemesOnLine[1:len(allLexemesOnLine)]
		printString = ""

		for lexeme in valueListLexemes:
			# If Lexeme token is any type of identifier EXCEPT string type identifiers
			if lexeme.getToken().getNumCode() in (2, 3, 5, 6, 7, 9):
				printString += str(self.getVarValue(lexeme.getLexemeString()))
			# If Lexeme token is string identifier or constant string identifier
			elif lexeme.getToken().getNumCode() in (4, 8):
				printString += str(self.getStringLiteralTxt(self.getVarValue(lexeme.getLexemeString())))
			# If lexeme token is any type of literal EXCEPT a string literal
			elif lexeme.getToken().getNumCode() in (10, 11, 13):
				printString += str(lexeme.getLexemeString())
			# If lexeme token is a string literal
			elif lexeme.getToken() is Token.STRING_LITERAL:
				printString += str(self.getStringLiteralTxt(lexeme.getLexemeString()))

		return printString

	# Returns string value which excludes the quotes and comma
	def getStringLiteralTxt(self, lexemeStr):
		result = re.search("\"(.*)\"", lexemeStr)
		return result.group(1)

	# Interprets exp node and returns expression value
	def interpretExp(self, node):
		allLexemesOnLine = node.getScanLine().getLexemes()

		expLexemes = allLexemesOnLine[3:len(allLexemesOnLine)]

		# Creates priority dictionary to rank which operators are solved first
		priority = {"*": 1, "/": 1, "+": 2, "-": 2}

		lexemeList = []
		operList = []

		index = 0
		exprResult = 0

		for lexeme in expLexemes:
			if lexeme.getToken().getNumCode() in (2, 3, 6, 7, 10, 11):
				lexemeList.append(lexeme)
			elif lexeme.getToken().getNumCode() in (25, 26, 27, 28):
				while len(operList) != 0 and priority[operList[len(operList)-1]] <= priority[lexeme.getLexemeString()]:
					lexemeList.append(Lexeme(operList[len(operList)-1], Token.findToken(operList.pop())))
				operList.append(lexeme.getLexemeString())

		while len(operList) != 0:
			lexemeList.append(Lexeme(operList[len(operList) - 1], Token.findToken(operList.pop())))

		postFixList = []

		for lexeme in lexemeList:
			if lexeme.getToken() is Token.MUL_OPERATOR:
				self.mulOper(postFixList)
			elif lexeme.getToken() is Token.DIV_OPERATOR:
				self.divOper(postFixList)
			elif lexeme.getToken() is Token.ADD_OPERATOR:
				self.addOper(postFixList)
			elif lexeme.getToken() is Token.SUB_OPERATOR:
				self.subOper(postFixList)
			else:
				postFixList.append(lexeme.getLexemeString())

		return postFixList.pop()

	# Multiplies the two top elements in postFixList
	def mulOper(self, postFixList):
		varTwo = postFixList.pop()
		varOne = postFixList.pop()

		valOne = None
		valTwo = None

		# Find value of first variable
		if Token.findToken(varOne) is Token.INTEGER_LITERAL:
			valOne = int(varOne)
		elif Token.findToken(varOne) is Token.FLOAT_LITERAL:
			valOne = float(varOne)
		else:
			varOneType = self.getVarType(varOne)
			if varOneType is Token.INTEGER:
				valOne = int(self.getVarValue(varOne))
			elif varOneType is Token.FLOAT:
				valOne = float(self.getVarValue(varOne))

		# Find value of second variable
		if Token.findToken(varTwo) is Token.INTEGER_LITERAL:
			valTwo = int(varTwo)
		elif Token.findToken(varTwo) is Token.FLOAT_LITERAL:
			valTwo = float(varTwo)
		else:
			varTwoType = self.getVarType(varTwo)
			if varTwoType is Token.INTEGER:
				valTwo = int(self.getVarValue(varTwo))
			elif varTwoType is Token.FLOAT:
				valTwo = float(self.getVarValue(varTwo))

		result = valOne * valTwo
		postFixList.append(str(result))

	# Divides the two top elements in postFixList
	def divOper(self, postFixList):
		varTwo = postFixList.pop()
		varOne = postFixList.pop()

		valOne = None
		valTwo = None

		# Find value of first variable
		if Token.findToken(varOne) is Token.INTEGER_LITERAL:
			valOne = int(varOne)
		elif Token.findToken(varOne) is Token.FLOAT_LITERAL:
			valOne = float(varOne)
		else:
			varOneType = self.getVarType(varOne)
			if varOneType is Token.INTEGER:
				valOne = int(self.getVarValue(varOne))
			elif varOneType is Token.FLOAT:
				valOne = float(self.getVarValue(varOne))

		# Find value of second variable
		if Token.findToken(varTwo) is Token.INTEGER_LITERAL:
			valTwo = int(varTwo)
		elif Token.findToken(varTwo) is Token.FLOAT_LITERAL:
			valTwo = float(varTwo)
		else:
			varTwoType = self.getVarType(varTwo)
			if varTwoType is Token.INTEGER:
				valTwo = int(self.getVarValue(varTwo))
			elif varTwoType is Token.FLOAT:
				valTwo = float(self.getVarValue(varTwo))

		result = valOne / valTwo
		postFixList.append(str(result))

	# Adds the two top elements in postFixList
	def addOper(self, postFixList):
		varTwo = postFixList.pop()
		varOne = postFixList.pop()

		valOne = None
		valTwo = None

		# Find value of first variable
		if Token.findToken(varOne) is Token.INTEGER_LITERAL:
			valOne = int(varOne)
		elif Token.findToken(varOne) is Token.FLOAT_LITERAL:
			valOne = float(varOne)
		else:
			varOneType = self.getVarType(varOne)
			if varOneType is Token.INTEGER:
				valOne = int(self.getVarValue(varOne))
			elif varOneType is Token.FLOAT:
				valOne = float(self.getVarValue(varOne))

		# Find value of second variable
		if Token.findToken(varTwo) is Token.INTEGER_LITERAL:
			valTwo = int(varTwo)
		elif Token.findToken(varTwo) is Token.FLOAT_LITERAL:
			valTwo = float(varTwo)
		else:
			varTwoType = self.getVarType(varTwo)
			if varTwoType is Token.INTEGER:
				valTwo = int(self.getVarValue(varTwo))
			elif varTwoType is Token.FLOAT:
				valTwo = float(self.getVarValue(varTwo))

		result = valOne + valTwo
		postFixList.append(str(result))

	# Subtracts the two top elements in postFixList
	def subOper(self, postFixList):
		varTwo = postFixList.pop()
		varOne = postFixList.pop()

		valOne = None
		valTwo = None

		# Find value of first variable
		if Token.findToken(varOne) is Token.INTEGER_LITERAL:
			valOne = int(varOne)
		elif Token.findToken(varOne) is Token.FLOAT_LITERAL:
			valOne = float(varOne)
		else:
			varOneType = self.getVarType(varOne)
			if varOneType is Token.INTEGER:
				valOne = int(self.getVarValue(varOne))
			elif varOneType is Token.FLOAT:
				valOne = float(self.getVarValue(varOne))

		# Find value of second variable
		if Token.findToken(varTwo) is Token.INTEGER_LITERAL:
			valTwo = int(varTwo)
		elif Token.findToken(varTwo) is Token.FLOAT_LITERAL:
			valTwo = float(varTwo)
		else:
			varTwoType = self.getVarType(varTwo)
			if varTwoType is Token.INTEGER:
				valTwo = int(self.getVarValue(varTwo))
			elif varTwoType is Token.FLOAT:
				valTwo = float(self.getVarValue(varTwo))

		result = valOne * valTwo
		postFixList.append(str(result))

	# Looks up the stored value of the variable identity lexeme
	def getVarValue(self, varIdent):
		varVal = None

		if str(varIdent) in self.globalVariables:
			varVal = self.globalVariables[str(varIdent)][0]
		elif str(varIdent) in self.globalConstants:
			varVal = self.globalConstants[str(varIdent)][0]
		elif str(varIdent) in self.implementVariables:
			varVal = self.implementVariables[str(varIdent)][0]
		elif str(varIdent) in self.implementConstants:
			varVal = self.implementConstants[str(varIdent)][0]

		return varVal

	# Looks up the stored type of the variable identity lexeme
	def getVarType(self, varIdent):
		varType = None

		if str(varIdent) in self.globalVariables:
			varType = self.globalVariables[str(varIdent)][1]
		elif str(varIdent) in self.globalConstants:
			varType = self.globalConstants[str(varIdent)][1]
		elif str(varIdent) in self.implementVariables:
			varType = self.implementVariables[str(varIdent)][1]
		elif str(varIdent) in self.implementConstants:
			varType = self.implementConstants[str(varIdent)][1]

		return varType

	# Returns true if variable identity lexeme is a number
	def isNumber(self, varIdent):
		varType = self.getVarType(varIdent)

		if varType is Token.INTEGER or varType is Token.FLOAT:
			return True
		else:
			return False
