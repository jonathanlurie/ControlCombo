# a mapping item is an association between four things:
# a LETTER is the row index,
# a FIGURE is the column index,
# a STATE is P for pressed or R for released,
# a ARGUMENT is the keyboard mapping key

import re

class MappingItem:

	m_originalString = None
	m_mapKey = None
	m_mapArgument = None
	m_isValid = False

	def __init__(self, theOrigString):
		self.m_originalString = theOrigString
		self.checkIntegrity()

	def getMapKey(self):
		return self.m_mapKey;

	def getMapAgument(self):
		return self.m_mapArgument;

	def checkIntegrity(self):
		# use split('\t') instead, in order to be able to use space character in the argument part (last)
		tempArray = self.m_originalString.split('\t')

		# 1st condition: there must be 4 elements in the array
		if(len(tempArray) == 4):
			# 2nd condition: the first element must be a letter
			if(tempArray[0].isalpha()):
				self.m_RowIndex = tempArray[0]

				# 3rd condition: the second must be a digit
				if(tempArray[1].isdigit()):
					self.m_columnIndex = int(tempArray[1])

					# 4th condition: the 3rd element must be P, p, R, or r
					# TODO: add Hh to this regex in order to take HOLD signal in consideration
					if( re.match("^[PpRrHh]*$", tempArray[2]) and len(tempArray[2]) == 1  ):
						self.m_mapKey = str(tempArray[0]) + str(tempArray[1]) + str(tempArray[2]).upper()
						self.m_mapArgument = tempArray[3]
						self.m_isValid = True

	def printInfo(self):
		print("Original string: " + self.m_originalString)
		print("Map argument: " + self.m_mapArgument)
		print("Map key: " + self.m_mapKey)

	def IsValid(self):
		return self.m_isValid
