# serial port reading
import serial
import os
import pythoncom

from time import sleep

# project import
from CommandInterpreter import *

class SerialMatrixReader:

	m_serial = None
	
	m_numberOfRow = None # to be read
	m_numberOfColumns = None  # to be read
	
	m_commandInterpreter = None  # in charge of launching some actions
	m_serialPortList = None

	def __init__(self):
		self.m_serialPortList = []
		
		print("INFO: Scanning port...")
		# scanning port
		self._serial_ports()
	
		print("INFO: port " + self.m_serialPortList[0] + "  detected!")
	
		# connetion to serial device
		self.m_serial = serial.Serial(self.m_serialPortList[0], 9600)
		
		# guessing the matrix size
		self._findMatrixSize()
	
	# Returns a generator for all available serial ports
	def _serial_ports(self):
		if os.name == 'nt':
			# windows
			for i in range(256):
				try:
					s = serial.Serial(i)
					s.close()
					#yield 'COM' + str(i + 1)
					self.m_serialPortList.append('COM' + str(i + 1))
				except serial.SerialException:
					pass
	
	
	def setCommandInterpreter(self, ci):
		self.m_commandInterpreter = ci
	
	# by reading some redundant messages from
	# the serial device...
	def _findMatrixSize(self):
		
		sizeFound = False
		splitedString = None
		
		while(not sizeFound):
			message = self.m_serial.readline().strip()
			
			# the message must contain the sizes
			if( "NB_ROW" in message and "NB_COLUMNS" in message):
				splitedString = message.split()
				
				# getting those sizes
				for i in range(len(splitedString)):
					if(splitedString[i] == "NB_ROW"):
						self.m_numberOfRow = int(splitedString[i+1])
				
					if(splitedString[i] == "NB_COLUMNS"):
						self.m_numberOfColumns = int(splitedString[i+1])
			
			if(self.m_numberOfColumns and self.m_numberOfRow):
				sizeFound = True
				
		print("INFO: Matrix size found:  columns: " + str(self.m_numberOfColumns) + "  rows: " + str(self.m_numberOfRow))
	
	
	# convert the input serial integer to a mapping key like A1P
	def _convertMatrixSignalToMapKey(self, signal):
		
		pushOrReleasedOrHold = None
		
		# if signal is greater (or equal to) than 1000
		# it means HOLD (1000 for 1, 2000 for 2, etc.)
		if(signal >= 1000):
			buttonIndex = signal / 1000
			pushOrReleasedOrHold = "H"
		else:
			buttonIndex = abs(signal) # convert to an unsigned index of the button among the matrix
			
			if(buttonIndex != signal):
				pushOrReleasedOrHold = "P"
			else:
				pushOrReleasedOrHold = "R"
	
		
				
		# compute the indexes of row and columns
		columnIndex = ((buttonIndex-1) % self.m_numberOfColumns) +1
		rowIndex = int((buttonIndex-1) / self.m_numberOfColumns) 
		
		# convert the row index to letter
		rowIndexxAlpha = chr(rowIndex + 97).upper()
			
		# concatenate to make the mapKey
		mapKey = rowIndexxAlpha + str(columnIndex) + pushOrReleasedOrHold
		
		return mapKey
		
	
	def readFlow(self):
		# if the sizes were found
		if(self.m_numberOfColumns and self.m_numberOfRow):
		
			while(True):
				try: 
					message = self.m_serial.readline().strip()
				
					try: # convert the matrix signal to integer
						buttonMessage = int(message) # signed
						mapKey = self._convertMatrixSignalToMapKey(buttonMessage)
					
						self.m_commandInterpreter.executeCommandFromKey(mapKey)
						#print(mapKey)
					
					except ValueError: # failed at converting the matrix signal to integer
						#print("INFO: this key is not assignated")
						none = None
		
				except KeyboardInterrupt:
					print("WARNING: you're such a keyboard ninja!")
					exit()
			
		