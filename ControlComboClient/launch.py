# serial port reading
import serial

# data container
from collections import Counter

# keyboard shortcut execution
import win32com.client

# project imports
from KeyMapReader import *
from SerialMatrixReader import *
from CommandInterpreter import *



try:
	# creating the key map reader, in charge of reading the
	# instruction from the .setting file
	kmr = KeyMapReader()
	kmr.setMapFileName("input\map.setting")
	kmr.readMapFile()

	# creating the command interpreter
	ci = CommandInterpreter()
	# giving the key-argument map to the command interpreter:
	ci.setKeyArgumentMap(  kmr.getKeyArgumentMap() )

	# creating the serial matrix reader, in charge of catching
	# the messages from the tangible matrix
	smr = SerialMatrixReader()
	smr.setCommandInterpreter(ci)
	smr.readFlow()

except KeyboardInterrupt:
	exit()
