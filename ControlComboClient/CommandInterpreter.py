# CommandInterpreter knows everything: the mapped key,
# the arguments linked to them and finally the instruction
# given by the matrix buttons

import sys
import threading

# keyboard shortcut execution
import win32com.client

# importing local plugins
sys.path.append(".\\plugins")

from ThreadedPluginManager import *

class CommandInterpreter:

	m_keyArgumentMap = None  # the keyArgument map given by KeyMapReader
	m_virtualKeyboard = None  # object that simulate keyboard
	m_pluginMethodMap = {}  # contains all the dynamic method from plugins
	m_pluginThreadMap = {}  # contains all the dynamic method from plugins
	m_pluginMap = {}
	
	
	def __init__(self):
		self.m_virtualKeyboard = win32com.client.Dispatch("WScript.Shell")
	
	def setKeyArgumentMap(self, map):
		self.m_keyArgumentMap = map;
		self._registerPlugins()
	
	def _registerPlugins(self):
		# loop over the arguments, looking for some plugins
		for it in self.m_keyArgumentMap.values():
			# try to construct a plugin from that
			tempThreadedPlugin = ThreadedPluginManager(it)
			
			# if valid, we load it and add it to the plugin dictionary
			if(tempThreadedPlugin.hasAValidFormat()):
				try:
					tempThreadedPlugin.loadPlugin()
					self.m_pluginMap[it] = tempThreadedPlugin
				except Exception, e:
					print("\nERROR: " + str(e) + "\n")
	# launch a plugin
	# pluginString must be formatted like that: plugin|pluginName|pluginFunction
	# to work.
	# Returns True if the plugin method was launched
	# Returns False if not (meaning it has to be considered as a keyboard shortcut)
	def _launchPluginMethod(self, pluginString):
		# does the pluginString exist in the plugin map?
		if(pluginString in self.m_pluginMap.keys()):
			# was it instantiated?
			if(self.m_pluginMap[pluginString].isValid()):
				# launch it!
				self.m_pluginMap[pluginString].runPlugin()

				return True
			else:
				print("WARNING: the plugin method " + pluginString + " is not instantiated.")
				
		return False
	
	

	# given a key k, execute a command
	def executeCommandFromKey(self, k):
		print("key: " + k)
		
		# is this element in the map?
		if(k in self.m_keyArgumentMap):
			argument = self.m_keyArgumentMap[k]
			print("argument: " + argument)
			
			# if argument does not refer to a plugin, launch the keyboard shortcut mode
			if(not self._launchPluginMethod(argument)):
				self.executeVirtualKeyboardCommand( argument)
			
		else:
			print("WARNING: the command " + k + " is not defined in the .setting file.\n")
		
		
	# execute a keyboard shortcut with win32com
	def executeVirtualKeyboardCommand(self, c):
		self.m_virtualKeyboard.SendKeys(c)
		
		
		
		
		
		