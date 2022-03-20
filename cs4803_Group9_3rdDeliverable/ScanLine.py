

class ScanLine:

	# Constructor
	# Parameters: lineNum : line number of source program,
					# lineStr : raw text from source line,
					# lexemes : list of Lexeme objects detected in source line
	def __init__(self, lineNum, lineStr, lexemes):
		self.lineNum = lineNum
		self.lineStr = lineStr
		self.lexemes = lexemes

	def getLineNum(self):
		return self.lineNum

	def getLineStr(self):
		return self.lineStr

	def getLexemes(self):
		return self.lexemes

	def setLineNum(self, lineNum):
		self.lineNum = lineNum

	def setLineStr(self, lineStr):
		self.lineStr = lineStr

	def setLexemes(self, lexemes):
		self.lexemes = lexemes
