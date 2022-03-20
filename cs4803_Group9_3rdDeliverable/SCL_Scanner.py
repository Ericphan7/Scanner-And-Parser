

from Token import Token
from ScanLine import ScanLine
from Lexeme import Lexeme


class SCL_Scanner(object):

	# Constructor
	# Parameters: sclFilePath : File path string to source SCL file
	def __init__(self, sclFilePath):
		self.sclFilePath = sclFilePath
		self.scanLines = []

		self.globalConstants = {}
		self.globalVariables = {}
		# TODO: This will need to be revised as this needs to be localised per function not just in implementations to work with parser
		self.implementationVariables = {}

		# Automatically calls scan method upon instantiation
		self.scan()

	# Adds new ScanLine object to the end of the scanLines list
	# Parameters: newScanLine : New ScanLine object
	# Returns: Void
	def addScanLine(self, newScanLine):
		self.scanLines.append(newScanLine)

	# Resets scanLines list to zero elements
	# Returns: Void
	def clearScanLines(self):
		self.scanLines = []

	# Returns list of ScanLine objects in Scanner
	def getScanLines(self):
		return self.scanLines

	# Modified version of str.split() which divides chars into elements by whitespace,
	# but retains STRING_LITERAL's in one singular element
	@staticmethod
	def modSplitLine(line):
		originalSplitLine = line.split()

		currentWordIndex = 0
		beginQuoteIndex = None
		endQuoteIndex = None

		newSplitLine = []

		for word in originalSplitLine:
			if word.find("\"") != -1:
				# If the word contains no spaces but is still a string literal
				if word[0] == "\"" and word[len(word) - 1] == "\"":
					newSplitLine.append(word)
				# If no string literal construction has been detected yet
				elif beginQuoteIndex is None:
					beginQuoteIndex = currentWordIndex
				# If string literal construction has been detected but not finished
				elif endQuoteIndex is None:
					endQuoteIndex = currentWordIndex

					# Append a joined string of every element from beginQuoteIndex to endQuoteIndex + 1
					newSplitLine.append(" ".join(originalSplitLine[beginQuoteIndex: endQuoteIndex + 1]))
					beginQuoteIndex = None
					endQuoteIndex = None


			# If there is not an ongoing string detection
			elif beginQuoteIndex is None and endQuoteIndex is None:
				newSplitLine.append(word)

			currentWordIndex += 1

		return newSplitLine

	# Modifies the ScanLine objects to include the detected Lexemes
	# Returns: Void
	def scan(self):

		# Opens scl file in read-only mode
		sclFile = open(self.sclFilePath, "r")

		globalConstants = {}
		globalVariables = {}
		implementationVariables = {}

		# Verify that sclFIle is in read-only mode
		if (sclFile.mode == "r"):
			lines = sclFile.readlines()

			lineNumber = 1
			constantsMode = False
			variablesMode = False
			implementationsMode = False

			# Iterate through each line in the file
			for line in lines:

				# Creates an array of words separated by white-space
				splitLine = SCL_Scanner.modSplitLine(line)

				# Reformats line into new variable that removes the "tabs"
				trimmedLine = line.strip('    ')

				# Holds lexeme objects found in line
				lexemes = []

				lineSize = len(splitLine)

				firstWord = splitLine[0] if lineSize >= 1 else ""
				secondWord = splitLine[1] if lineSize >= 2 else ""
				thirdWord = splitLine[2] if lineSize >= 3 else ""
				fourthWord = splitLine[3] if lineSize >= 4 else ""

				# Iterate through each word in the splitLine list
				for word in splitLine:
					detectedToken = Token.findToken(word)

					if word == firstWord:
						if detectedToken == Token.CONSTANTS:
							constantsMode = True
							variablesMode = False
							implementationsMode = False
						elif detectedToken == Token.VARIABLES and implementationsMode is False:
							constantsMode = False
							variablesMode = True
							implementationsMode = False
						elif detectedToken == Token.IMPLEMENTATIONS:
							constantsMode = False
							variablesMode = False
							implementationsMode = True

						lexemes.append(Lexeme(word, detectedToken))
						continue

					elif word == secondWord:

						# If the detectedToken has a specified Token value
						if detectedToken is not Token.NOT_DEFINED:
							lexemes.append(Lexeme(word, detectedToken))

						# If the detectedToken is NOT_DEFINED
						else:
							if Token.findToken(firstWord) == Token.SYMBOL:
								lexemes.append(Lexeme(word, Token.SYMBOL_IDENTIFIER))

							elif Token.findToken(firstWord) == Token.END_FUN:
								lexemes.append(Lexeme(word, Token.FUNCTION_IDENTIFIER))

							elif Token.findToken(firstWord) == Token.DEFINE:
								lastWord = splitLine[lineSize-1]

								# Global Variables
								if variablesMode is True and constantsMode is False and implementationsMode is False:
									if Token.findToken(lastWord) == Token.INTEGER:
										lexemes.append(Lexeme(word, Token.INTEGER_IDENTIFIER))
										globalVariables[word] = Token.INTEGER_IDENTIFIER
									elif Token.findToken(lastWord) == Token.FLOAT:
										lexemes.append(Lexeme(word, Token.FLOAT_IDENTIFIER))
										globalVariables[word] = Token.FLOAT_IDENTIFIER
									elif Token.findToken(lastWord) == Token.STRING:
										lexemes.append(Lexeme(word, Token.STRING_IDENTIFIER))
										globalVariables[word] = Token.STRING_IDENTIFIER
									elif Token.findToken(lastWord) == Token.BOOLEAN:
										lexemes.append(Lexeme(word, Token.BOOLEAN_IDENTIFIER))
										globalVariables[word] = Token.BOOLEAN_IDENTIFIER

								# Global Constants
								if variablesMode is False and constantsMode is True and implementationsMode is False:
									if Token.findToken(lastWord) == Token.INTEGER:
										lexemes.append(Lexeme(word, Token.CONSTANT_INTEGER_IDENTIFIER))
										globalConstants[word] = Token.CONSTANT_INTEGER_IDENTIFIER
									elif Token.findToken(lastWord) == Token.FLOAT:
										lexemes.append(Lexeme(word, Token.CONSTANT_FLOAT_IDENTIFIER))
										globalConstants[word] = Token.CONSTANT_FLOAT_IDENTIFIER
									elif Token.findToken(lastWord) == Token.STRING:
										lexemes.append(Lexeme(word, Token.CONSTANT_STRING_IDENTIFIER))
										globalConstants[word] = Token.CONSTANT_STRING_IDENTIFIER
									elif Token.findToken(lastWord) == Token.BOOLEAN:
										lexemes.append(Lexeme(word, Token.CONSTANT_BOOLEAN_IDENTIFIER))
										globalConstants[word] = Token.CONSTANT_BOOLEAN_IDENTIFIER

								# Implementations Variables
								if variablesMode is False and constantsMode is False and implementationsMode is True:
									if Token.findToken(lastWord) == Token.INTEGER:
										lexemes.append(Lexeme(word, Token.INTEGER_IDENTIFIER))
										implementationVariables[word] = Token.INTEGER_IDENTIFIER
									elif Token.findToken(lastWord) == Token.FLOAT:
										lexemes.append(Lexeme(word, Token.FLOAT_IDENTIFIER))
										implementationVariables[word] = Token.FLOAT_IDENTIFIER
									elif Token.findToken(lastWord) == Token.STRING:
										lexemes.append(Lexeme(word, Token.STRING_IDENTIFIER))
										implementationVariables[word] = Token.STRING_IDENTIFIER
									elif Token.findToken(lastWord) == Token.BOOLEAN:
										lexemes.append(Lexeme(word, Token.BOOLEAN_IDENTIFIER))
										implementationVariables[word] = Token.BOOLEAN_IDENTIFIER

							# TODO: Review this later. May not be needed anymore
							elif Token.findToken(firstWord) == Token.SET:
								# lexemes.append(Lexeme(word, Token.IDENTIFIER))
								if word in globalConstants:
									lexemes.append(Lexeme(word, globalConstants[word]))
								elif word in globalVariables:
									lexemes.append(Lexeme(word, globalVariables[word]))
								elif word in implementationVariables:
									lexemes.append(Lexeme(word, implementationVariables[word]))
								else:
									lexemes.append(
										Lexeme(word, Token.IDENTIFIER))  # TODO: Need to get rid of IDENTIFIER

							elif Token.findToken(firstWord) == Token.IMPORT:
									if detectedToken is Token.STRING_LITERAL:
										lexemes.append(Lexeme(word, Token.STRING_LITERAL))
									else:
										lexemes.append(Lexeme(word, Token.NOT_DEFINED))

							elif Token.findToken(firstWord) == Token.FUNCTION:
								lexemes.append(Lexeme(word, Token.FUNCTION_IDENTIFIER))

						continue

					if Token.findToken(word) != Token.NOT_DEFINED:
						lexemes.append(Lexeme(word, Token.findToken(word)))
						continue

					if Token.findToken(word) == Token.NOT_DEFINED:
						if word in globalConstants:
							lexemes.append(Lexeme(word, globalConstants[word]))
						elif word in globalVariables:
							lexemes.append(Lexeme(word, globalVariables[word]))
						elif word in implementationVariables:
							lexemes.append(Lexeme(word, implementationVariables[word]))
						else:
							lexemes.append(Lexeme(word, Token.IDENTIFIER)) # TODO: Need to get rid of IDENTIFIER
						continue

				scanLine = ScanLine(lineNumber, trimmedLine, lexemes)
				self.addScanLine(scanLine)
				lineNumber += 1

		self.globalConstants = globalConstants
		self.globalVariables = globalVariables
		self.implementationVariables = implementationVariables
		sclFile.close()
