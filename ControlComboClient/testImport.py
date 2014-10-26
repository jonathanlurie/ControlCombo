
import sys
#import urllib
sys.path.append(".\\plugins")




m_pluginMethodMap = {}


# return None is not,
# a list containing module and method to call
def isPluginArgument(argum):
	returnTab = None

	splited = argum.split("|")
	
	# does it contain 3 parts?
	if (len(splited) == 3):
		# is the firt of them is "plugin" ?
		if(splited[0].upper() == "PLUGIN"):
			returnTab = list()
			returnTab.append(splited[1].strip())
			returnTab.append(splited[2].strip())
			
	return returnTab


# load the duet Module|method into a dictionary
def _addToPuginMap(pgn):
	try:
		# loading the plugin
		tempModule = __import__( pgn[0], pg[1])
	
		try:
			m_pluginMethodMap["plugin|" + pgn[0] + "|" +pg[1]] = getattr(tempModule, pg[1])
		except AttributeError:
			print("ERROR: not able to import method " + pg[0]  + "." + pg[1] + "()")
			m_pluginMethodMap["plugin|" + pgn[0] + "|" +pg[1]]= None
	
	except ImportError:
		print("not able to import module " + samplePlugin )
		m_pluginMethodMap["plugin|" + pgn[0] + "|" +pg[1]]= None
	
	
# launch a plugin
# pluginString must be formatted like that: plugin|pluginName|pluginFunction
# to work.
# Returns True if the plugin method was launched
# Returns False if not (meaning it has to be considered as a keyboard shortcut)
def launchPluginMethod(pluginString):
	# does the pluginString exist in the plugin map?
	if(pluginString in m_pluginMethodMap.keys()):
		# was it instantiated?
		if(m_pluginMethodMap[pluginString]):
			m_pluginMethodMap[pluginString]()
			return True
		else:
			print("WARNING: the plugin method " + pluginString + " is not instantiated.")
			
	return False
	
	
argument = "plugin|samplePlugin|helloYou"

# testing the argument as a plugin
pg = isPluginArgument(argument)
		
if( pg ):
	# add it to the plugin map
	_addToPuginMap(pg)
	


launchPluginMethod(argument)


