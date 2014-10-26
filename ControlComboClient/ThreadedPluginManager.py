# load a plugin, check its integrity, deals with its arguments, launch it on a threaded way.
import threading

import inspect

class ThreadedPluginManager:

	# considering the plugin string, say if its format is valid
	m_hasValidFormat = False
	
	# once the string format is valid, when trying to load the module/function
	# if it works, m_isValid switches to True
	m_isValid = False
	
	# name of the Python module to load (contains the threadedFuncion)
	m_moduleName = None
	m_functionName = None
	
	m_moduleObject = None
	m_fuctionObject = None
	m_threadObject = None
	m_arguments = ()

	# the constructor take a pluginString, wich is formated string for plugin.
	# must be like plugin|pluginName|pluginFunction to be valid.
	# 
	def __init__(self, pluginString):
			splited = pluginString.split("|")
			# does it contain 3 parts?
			if (len(splited) >= 3):
				# is the firt of them is "plugin" ?
				if(splited[0].upper() == "PLUGIN"):
					self.m_hasValidFormat = True
					
					# remembering there names
					self.m_moduleName = splited[1].strip()
					self.m_functionName = splited[2].strip()
					
					# taking the arguments
					if(len(splited) > 3):
						for i in range(3, len(splited)):
							#self.m_arguments.append(splited[i].strip())
							self.m_arguments = self.m_arguments +  (splited[i].strip(), )
							
					
					
	# return if the plugin string was valid.
	# does not consider the actual existence of the plugin!
	def hasAValidFormat(self):
		return self.m_hasValidFormat
	
	# does the couple module/method was able to be loaded?
	def isValid(self):
		return self.m_isValid
	
	
	# loads the plugin in order to launch it later
	def loadPlugin(self):
		try:
			# loading the plugin
			self.m_moduleObject = __import__( self.m_moduleName, self.m_functionName)
		
			try:
				self.m_fuctionObject = getattr(self.m_moduleObject, self.m_functionName)
				
				# check is number of arguments is ok with what we have
				nbArgForPlugin = len(inspect.getargspec(self.m_fuctionObject).args)
				if( nbArgForPlugin != len(self.m_arguments) ):
					raise Exception("The plugin "+ self.m_moduleName + "." + self.m_functionName + " takes " + str(nbArgForPlugin) + " arguments! ( " + str(len(self.m_arguments)) + " given)" )
				else:
					self.m_isValid = True # the only case the plugin is valid
					
			except AttributeError:
				raise Exception("Unable to import the method " + self.m_moduleName  + "." + self.m_functionName + "()")
				self.m_isValid = False
		except ImportError:
			raise Exception("Unable to import the module " +  self.m_moduleName)
			self.m_isValid = False
			
		
	
	# run the plugin (already loaded by loadPlugin)
	def runPlugin(self):
		# only if it is valid
		if(self.m_isValid):
		
			# if the thread for this plugin is not created or not alive anymore
			if(self.m_threadObject == None or not self.m_threadObject.isAlive()):
				self.m_threadObject = threading.Thread(None , self.m_fuctionObject , args = self.m_arguments )
				self.m_threadObject.start()

			else:
				print("INFO: threaded plugin " + self.m_moduleName + "." + self.m_functionName + " is already launched.")
		
		else:
			print("ERROR: invalid plugin, unable to run.")
			
		
		
		
		
		
		
		
		
		
		
		
		
		