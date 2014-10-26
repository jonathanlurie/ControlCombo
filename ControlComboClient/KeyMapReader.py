from MappingItem import *

# tuto de list:
# http://effbot.org/zone/python-list.htm


class KeyMapReader:
	
	m_mapFileName = None
	m_hasRead = False
	m_keyArgumentMap = {}  # contains all the valid MappingItems, it is a dictionary
	
	def __init__(self):
		print("")
		
	def setMapFileName(self, fileName):
		self.m_mapFileName = fileName
	
	# reads every line of the mapping file
	def readMapFile(self):
		# open the file
		with open(self.m_mapFileName) as fp:
			for line in fp:
				# read a line
				currentLine = line.strip()
				if(len(currentLine)>0 and currentLine[0] != "#" ):   # the line is not a comment...
					tempMappingItem = MappingItem(currentLine)
					
					# adding the map item
					if(tempMappingItem.IsValid()):
						self.m_keyArgumentMap[tempMappingItem.getMapKey()] = tempMappingItem.getMapAgument()
					else:
						tempMappingItem = None
	
		#print(self.m_keyArgumentMap)
		
		
	def getKeyArgumentMap(self):
		return self.m_keyArgumentMap