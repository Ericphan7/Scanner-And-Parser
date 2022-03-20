

from SCL_Scanner import SCL_Scanner
from Node import Node
from Token import Token
from Tree import Tree
from NodeType import NodeType


class SCL_Parser(SCL_Scanner):

	# Single argument constructor
	def __init__(self, sclFilePath):
		SCL_Scanner.__init__(self, sclFilePath)
		self.currentLineNum = 0
		self.lexemeNumber = 0
		self.currentToken = None
		self.scanLines = super().getScanLines()
		self.printLines = []

	# Method will perform syntax analysis
	def parse(self):
		root = Node(None, None, NodeType.PROGRAM)
		self.modPrint("Parsing " + str(root.getNodeType().value))

		lexeme = self.nextLexeme()

		self.currentToken = lexeme.getToken()
		# self.modPrint(lexeme.getLexemeString())
		while self.currentLineNum < len(self.scanLines) - 1:
			if self.currentToken is Token.IMPORT:
				self.parseImport(root)
				continue
			elif self.currentToken is Token.SYMBOL:
				self.parseSymbol(root)
				continue
			elif self.currentToken is Token.GLOBAL:
				self.parseGlobal(root)
				continue
			elif self.currentToken is Token.IMPLEMENTATIONS:
				self.parseImplementations(root)
				continue
			else:
				self.nextToken()

		self.modPrint("Finished parsing " + str(root.getNodeType().value))
		return Tree(root)

	# Method will both print statement and will append statement to self.printLines
	def modPrint(self, txt):
		print(str(txt))
		self.printLines.append(str(txt));

	# Iterates to the next lexeme in the source file
	def nextLexeme(self):
		# If current lexeme is the last lexeme on the line
		if self.lexemeNumber > len(self.scanLines[self.currentLineNum].getLexemes()) - 1:
			self.currentLineNum += 1
			self.lexemeNumber = 0

		# If current line is before the last line
		if self.currentLineNum < len(self.scanLines) - 1:
			# While current line is empty
			while len(self.scanLines[self.currentLineNum].getLexemes()) == 0 or self.currentLineNum > len(self.scanLines) - 1:
				self.currentLineNum += 1
		# else:
		# 	return Lexeme("", Token.NOT_DEFINED)

		result = self.scanLines[self.currentLineNum].getLexemes()[self.lexemeNumber]
		self.lexemeNumber += 1
		return result

	# Changes the value of currentToken to the Token value of the current lexeme
	def nextToken(self):
		self.currentToken = self.nextLexeme().getToken()

	# Prints the current line number, parameterized reason for error, and line string
	def errorMsg(self, reason=""):
		msg = "Error at line " + str(self.currentLineNum) + ": \n"
		msg += "Reason: " + str(reason) + "\n\t\""
		msg += self.scanLines[self.currentLineNum].getLineStr()[0:-1] + "\""
		self.modPrint(msg)

	# Parses <import_stmnt>
	def parseImport(self, node):
		importNode = Node(node, self.scanLines[self.currentLineNum], NodeType.IMPORT)
		node.addChildNode(importNode)
		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(importNode.getNodeType().value))

		self.nextToken()

		if self.currentToken is not Token.STRING_LITERAL:
			self.errorMsg("Missing Import String value.")
			node.removeChildNode(node.getChildren()[len(node.getChildren())-1])
			return None

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(importNode.getNodeType().value))

	# Parses <symbol_stmnt>
	def parseSymbol(self, node):
		symbolNode = Node(node, self.scanLines[self.currentLineNum], NodeType.SYMBOL)
		node.addChildNode(symbolNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(symbolNode.getNodeType().value))

		self.nextToken()

		if self.currentToken is not Token.SYMBOL_IDENTIFIER:
			self.errorMsg("Missing Symbol Identifier.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		self.nextToken()

		if self.currentToken is not Token.INTEGER_LITERAL:
			self.errorMsg("Missing Symbol value.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(symbolNode.getNodeType().value))

	# Parses <globals>
	def parseGlobal(self, node):
		globalNode = Node(node, self.scanLines[self.currentLineNum], NodeType.GLOBALS)
		node.addChildNode(globalNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(globalNode.getNodeType().value))

		self.nextToken()

		if self.currentToken is not Token.DECLARATIONS:
			self.errorMsg("Missing Declarations Keyword after Global.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None


		self.nextToken()
		if self.currentToken is Token.CONSTANTS:
			self.parseConstDec(globalNode)

		if self.currentToken is Token.VARIABLES:
			self.parseVarDec(globalNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(globalNode.getNodeType().value))

	# Parses <const_dec>
	def parseConstDec(self, node):
		constDecNode = Node(node, self.scanLines[self.currentLineNum], NodeType.CONST_DEC)
		node.addChildNode(constDecNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(constDecNode.getNodeType().value))

		self.nextToken()

		if self.currentToken is not Token.DEFINE:
			self.errorMsg("Missing Define keyword after constants.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		if self.currentToken is Token.DEFINE:
			self.parseConstList(constDecNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(constDecNode.getNodeType().value))

	# Parses <const_list>
	def parseConstList(self, node):
		constListNode = Node(node, self.scanLines[self.currentLineNum], NodeType.CONST_LIST)
		node.addChildNode(constListNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(constListNode.getNodeType().value))

		# self.nextToken()

		if self.currentToken is not Token.DEFINE:
			self.errorMsg("Missing Define keyword.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		while self.currentToken is Token.DEFINE:
			self.parseCompDeclare(constListNode)
			self.nextToken()

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(constListNode.getNodeType().value))

	# Parses <comp_declare>
	def parseCompDeclare(self, node):
		compDeclareNode = Node(node, self.scanLines[self.currentLineNum], NodeType.COMP_DECLARE)
		node.addChildNode(compDeclareNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(compDeclareNode.getNodeType().value))

		constantDeclare = False
		varDeclare = False


		self.nextToken()

		# If currentToken's numerical code doesn't match any of the identifier tokens (Between 2 and 9)
		if (2 <= self.currentToken.getNumCode() <= 9) is False:
			self.errorMsg("Missing variable name.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		if (2 <= self.currentToken.getNumCode() <= 5) is True:
			varDeclare = True

		if (6 <= self.currentToken.getNumCode() <= 9) is True:
			constantDeclare = True

		self.nextToken()

		# If third token is not "=" and is not "of"
		if self.currentToken is not Token.ASSIGNMENT_OPERATOR and self.currentToken is not Token.OF:
			self.errorMsg("Invalid third entry.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		self.nextToken()

		# If fourth token is not a literal and is not "type"
		if (10 <= self.currentToken.getNumCode() <= 13) is False and self.currentToken is not Token.TYPE:
			self.errorMsg("Invalid fourth entry.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		if varDeclare is True:
			if self.currentToken is Token.TYPE:
				self.parseRetType(compDeclareNode)

		elif constantDeclare is True:
			self.nextToken()

			if self.currentToken is not Token.TYPE:
				self.errorMsg("Missing return type.")
				node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
				return None

			else:
				self.parseRetType(compDeclareNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(compDeclareNode.getNodeType().value))

	# Parses <ret_type>
	def parseRetType(self, node):
		retTypeNode = Node(node, self.scanLines[self.currentLineNum], NodeType.RET_TYPE)
		node.addChildNode(retTypeNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(retTypeNode.getNodeType().value))

		self.nextToken()

		if self.currentToken.getNumCode() <= 2000:
			self.errorMsg("Missing return type.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(retTypeNode.getNodeType().value))

	# Parses <var_dec>
	def parseVarDec(self, node):
		varDecNode = Node(node, self.scanLines[self.currentLineNum], NodeType.VAR_DEC)
		node.addChildNode(varDecNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(varDecNode.getNodeType().value))

		self.nextToken()

		if self.currentToken is not Token.DEFINE:
			self.errorMsg("Missing Define keyword.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		if self.currentToken is Token.DEFINE:
			self.parseVarList(varDecNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(varDecNode.getNodeType().value))

	# Parses <var_list>
	def parseVarList(self, node):
		varListNode = Node(node, self.scanLines[self.currentLineNum], NodeType.VAR_LIST)
		node.addChildNode(varListNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(varListNode.getNodeType().value))

		# self.nextToken()

		if self.currentToken is not Token.DEFINE:
			self.errorMsg("Missing Define keyword.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		while self.currentToken is Token.DEFINE:
			self.parseCompDeclare(varListNode)
			self.nextToken()

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(varListNode.getNodeType().value))

	# Parses <implement>
	def parseImplementations(self, node):
		implementationsNode = Node(node, self.scanLines[self.currentLineNum], NodeType.IMPLEMENT)
		node.addChildNode(implementationsNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(implementationsNode.getNodeType().value))

		self.nextToken()

		if self.currentToken is not Token.FUNCTION:
			self.errorMsg("Missing Function keyword.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		if self.currentToken is Token.FUNCTION:
			self.parseFunctList(implementationsNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(implementationsNode.getNodeType().value))

	# Parses <funct_list>
	def parseFunctList(self, node):
		functListNode = Node(node, self.scanLines[self.currentLineNum], NodeType.FUNCT_LIST)
		node.addChildNode(functListNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(functListNode.getNodeType().value))

		# self.nextToken()

		if self.currentToken is not Token.FUNCTION:
			self.errorMsg("Missing Function keyword.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		while self.currentToken is Token.FUNCTION:
			self.parseFunctBody(functListNode)
			# self.nextToken() # TODO: Uncomment if stable

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(functListNode.getNodeType().value))

	# Parses <funct_body>
	def parseFunctBody(self, node):
		functBodyNode = Node(node, self.scanLines[self.currentLineNum], NodeType.FUNCT_BODY)
		node.addChildNode(functBodyNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(functBodyNode.getNodeType().value))

		self.nextToken()

		if self.currentToken is not Token.FUNCTION_IDENTIFIER and self.currentToken is not Token.MAIN:
			self.errorMsg("Missing Function Identifier.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		self.nextToken()

		if self.currentToken is not Token.IS:
			self.errorMsg("Missing is keyword at end of line")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		self.nextToken()

		# Local Constants
		if self.currentToken is Token.CONSTANTS:
			self.parseConstDec(functBodyNode)
		# Local Variables
		if self.currentToken is Token.VARIABLES:
			self.parseVarDec(functBodyNode)

		if self.currentToken is not Token.BEGIN:
			self.errorMsg("Missing Begin keyword.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		if self.currentToken is Token.BEGIN:
			self.parsePActions(functBodyNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(functBodyNode.getNodeType().value))

	# Parses <pactions>
	def parsePActions(self, node):
		pActionsNode = Node(node, self.scanLines[self.currentLineNum], NodeType.PACTIONS)
		node.addChildNode(pActionsNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(pActionsNode.getNodeType().value))

		# self.nextToken()

		if self.currentToken is not Token.BEGIN:
			self.errorMsg("Missing Begin keyword.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		self.nextToken()

		if self.currentToken is not Token.SET and self.currentToken is not Token.INPUT and self.currentToken is not Token.DISPLAY:
			self.errorMsg("Invalid statement. Check first word.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		while self.currentToken is Token.SET or self.currentToken is Token.INPUT or self.currentToken is Token.DISPLAY:
			self.parseActionDef(pActionsNode)
			# self.nextToken()

		if self.currentToken is not Token.END_FUN:
			self.errorMsg("Missing endfun keyword.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		self.nextToken()

		if self.currentToken is not Token.MAIN and self.currentToken is not Token.FUNCTION_IDENTIFIER:
			self.errorMsg("Missing Function Identifier.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(pActionsNode.getNodeType().value))

	# Parses <action_def>
	def parseActionDef(self, node):
		actionDefNode = Node(node, self.scanLines[self.currentLineNum], NodeType.ACTION_DEF)
		node.addChildNode(actionDefNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(actionDefNode.getNodeType().value))

		# self.nextToken()

		if self.currentToken is Token.SET:
			self.nextToken()

			if (2 <= self.currentToken.getNumCode() <= 9) is False:
				self.errorMsg("Missing variable name.")
				node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
				return None

			self.nextToken()

			if self.currentToken is not Token.ASSIGNMENT_OPERATOR:
				self.errorMsg("Missing = operator.")
				node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
				return None

			self.nextToken()
			self.parseExp(actionDefNode)

		elif self.currentToken is Token.INPUT:
			self.nextToken()

			if self.currentToken is not Token.STRING_LITERAL:
				self.errorMsg("Missing string.")
				node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
				return None

			self.nextToken()

			if (2 <= self.currentToken.getNumCode() <= 9) is False:
				self.errorMsg("Missing variable name.")
				node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
				return None

			self.nextToken()

		elif self.currentToken is Token.DISPLAY:
			self.nextToken()
			self.parsePvarValueList(actionDefNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(actionDefNode.getNodeType().value))

	# Parses <exp>
	def parseExp(self, node):
		expNode = Node(node, self.scanLines[self.currentLineNum], NodeType.EXP)
		node.addChildNode(expNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(expNode.getNodeType().value))

		# self.nextToken()

		if (2 <= self.currentToken.getNumCode() <= 18) is False and (25 <= self.currentToken.getNumCode() <= 29) is False:
			self.errorMsg("Invalid token. Expected variable name or operator.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		while (2 <= self.currentToken.getNumCode() <= 18) is True or (25 <= self.currentToken.getNumCode() <= 29) is True:

			if (2 <= self.currentToken.getNumCode() <= 18) is False and (
					25 <= self.currentToken.getNumCode() <= 29) is False:
				self.errorMsg("Invalid token. Expected variable name or operator.")
				node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
				return None

			self.nextToken()

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(expNode.getNodeType().value))

	# Parses <pvar_value_list>
	def parsePvarValueList(self, node):
		pvarValueListNode = Node(node, self.scanLines[self.currentLineNum], NodeType.PVAR_VALUE_LIST)
		node.addChildNode(pvarValueListNode)

		self.modPrint(" " + "\t" * node.getDepth() + "Parsing " + str(pvarValueListNode.getNodeType().value))

		# self.nextToken()

		if (2 <= self.currentToken.getNumCode() <= 13) is False:
			self.errorMsg("Invalid token. Expected variable name or value.")
			node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
			return None

		while (2 <= self.currentToken.getNumCode() <= 13) is True:
			if (2 <= self.currentToken.getNumCode() <= 13) is False:
				self.errorMsg("Invalid token. Expected variable name or value.")
				node.removeChildNode(node.getChildren()[len(node.getChildren()) - 1])
				return None

			self.nextToken()

		self.modPrint(" " + "\t" * node.getDepth() + "Finished parsing " + str(pvarValueListNode.getNodeType().value))
