

class Node:

	# Constructor
	def __init__(self, parent, scanLine, nodeType):
		self.parent = parent
		self.children = None
		self.scanLine = scanLine
		self.nodeType = nodeType

	# Getter Methods for all fields
	def getParent(self):
		return self.parent

	def getChildren(self):
		return self.children

	def getScanLine(self):
		return self.scanLine

	def getNodeType(self):
		return self.nodeType

	# Setter Methods for all fields
	def setParent(self, parent):
		self.parent = parent

	def setChildren(self, children):
		self.children = children

	def setScanLine(self, scanLine):
		self.scanLine = scanLine

	def setNodeType(self, nodeType):
		self.nodeType = nodeType

	# Adds node object to children list
	def addChildNode(self, child):
		if self.children is None:
			self.children = []  # Convert to array from None type

		self.children.append(child)

	# Removes node object from children list
	def removeChildNode(self, child):
		if self.children is not None:
			self.children.remove(child)
			child.setParent(None)

	# Returns the distance from the root node
	def getDepth(self):
		if self.getParent() is None:
			return 0
		else:
			currentNode = self
			depth = 0
			while currentNode.getParent() is not None:
				depth += 1
				currentNode = currentNode.getParent()
			return depth
