import pythoncom
import win32com.client

def demo():
	# needed when you launch a COM script in a thread
	#pythoncom.CoInitialize()
	
	# opening photoshop (it is ok if psd is already open)
	psApp = win32com.client.Dispatch("Photoshop.Application")
	
	# get the current doc
	doc = psApp.activeDocument

	resizeFromHeight(doc, 500)
	
	
	"""
	 # Get the bottom-most layer
	layer = doc.ArtLayers[0]
	
	
	layer.AdjustBrightnessContrast(20,-15)
	"""
	
	# Ending the COM script of the thread
	#pythoncom.CoUninitialize()
	
	
#___________________________________________________________________
#
#					ArtLayers
#___________________________________________________________________

# return the number of layers on the doc
def getNumberOfArtLayers(doc):
	return doc.ArtLayers.Count
	
# return the Nth ArtLayer (with bound check)
def getTheNthArtLayer(doc, n):
	if(n>=0 and n<getNumberOfArtLayers(doc)):
		return doc.ArtLayers.ArtLayers[n]
	
# Adds an ArtLayer to the doc layer stack, and return it
def addArtLayer(doc):
	return doc.ArtLayers.Add()

# NOT TESTED	
# Returns the index of the ArtLayer al among the doc
def getArtLayerIndex(doc, al):
	return doc.ArtLayers.Index(al)

	
#___________________________________________________________________
#
#					Document
#___________________________________________________________________

def getDocumentWidth(doc):
	return doc.Width
	
def getDocumentHeight(doc):
	return doc.Height

# resizes the image with no check
def resizeImage(doc, width, height):
	doc.ResizeImage(width, height, 300, 4)
	
# resizes the image proportionality to the biggerSide
def resizeBiggerSide(doc, biggerSide):
	currentW = getDocumentWidth(doc)
	currentH = getDocumentHeight(doc)
	ratio = float(currentW) / float(currentH)
	
	# it is a landscape oriented
	if(currentW > currentH):
		newW = biggerSide
		newH = biggerSide / ratio
	else:
	# it is portrait oriented
		newH = biggerSide
		newW = biggerSide * ratio
	
	resizeImage(doc, newW, newH)
	
	
# resize proportionally
def resizeFromWitdh(doc, width):
	currentW = getDocumentWidth(doc)
	currentH = getDocumentHeight(doc)
	newH = width / ( float(currentW) / float(currentH)) 
	resizeImage(doc, width, newH)
	
# resize proportionally
def resizeFromHeight(doc, height):
	currentW = getDocumentWidth(doc)
	currentH = getDocumentHeight(doc)
	newW = height * ( float(currentW) / float(currentH)) 
	resizeImage(doc, newW, height)
	
	
	
	
	
	
	
#demo()