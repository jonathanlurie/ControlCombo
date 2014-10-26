#import win32com.client


# this example is taken from
# http://win32com.goermezer.de/content/view/287/284/
def listSelectedFiles():
	# look in the makepy output for IE for the 'CLSIDToClassMap'
	# dictionary, and find the entry for 'ShellWindows'
	clsid='{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
	ShellWindows=win32com.client.Dispatch(clsid)
 
	# a busy state can be detected:
	# while ShellWindows[0].Busy == False:
	# go in for-loop here
 
	for i in range(ShellWindows.Count):
		print ShellWindows[i].LocationURL
		for j in range(ShellWindows[i].Document.SelectedItems().Count):
			print '  ', ShellWindows[i].Document.SelectedItems().Item(j).Path
 
	# Be careful: Internet Explorer uses also the same CLSID. You should implement a detection!
	
	
import win32com.client as win32
import os
import win32ui	
import time
import win32gui

# this example is taken from
# 	http://stackoverflow.com/questions/21241708/python-get-a-list-of-selected-files-in-explorer-windows-7
def listSelectedFiles2():
	working_dir = os.getcwd()
	
	
	appID = "{9BA05972-F6A8-11CF-A442-00A0C90A8F39}"
	shellwindows = win32.Dispatch(appID)

	files = []
	
	#try:
	for window in range(shellwindows.count):
		window_URL = shellwindows[window].LocationURL
		
		print(window_URL)
		
		selected_files = shellwindows[window].Document.SelectedItems()
			
		for file in range(selected_files.Count):
			files.append(selected_files.Item(file).Path)
				
		print(files)
		
		
		# find the folder
		#if(window_URL.find("file:///")):
		#	window_dir = window_URL.split("///")[1]#.replace("/", "\\")
		
			
		
		"""
		if window_dir == working_dir:
			selected_files = shellwindows[window].Document.SelectedItems()
			
			for file in range(selected_files.Count):
				files.append(selected_files.Item(file).Path)
		"""	
	#except:
	#	win32ui.MessageBox("Close IE!", "Error")
		
	#del shellwindows
	
	return files
	
	
	
	"""
	try:
        for window in range(shellwindows.Count):
            window_URL = shellwindows[window].LocationURL
            window_dir = window_URL.split("///")[1].replace("/", "\\")
            if window_dir == working_dir:
                selected_files = shellwindows[window].Document.SelectedItems()
                for file in range(selected_files.Count):
                    files.append(selected_files.Item(file).Path)
    except:   #Ugh, need a better way to handle this one
        win32ui.MessageBox("Close IE!", "Error")
    del shellwindows

    return files
	"""
	
# focus: http://stackoverflow.com/questions/2335721/how-can-i-get-the-window-focused-on-windows-and-re-size-it
# win32gui python doc: http://docs.activestate.com/activepython/2.4/pywin32/win32gui.html
# win32 msdn doc: http://msdn.microsoft.com/en-us/library/ms633516(v=vs.85).aspx
def getFore():
	appID = "{9BA05972-F6A8-11CF-A442-00A0C90A8F39}"
	shellwindows2 = win32.Dispatch(appID)
	
	hwnd = win32gui.GetForegroundWindow()
	print(shellwindows2[hwnd].LocationURL)
	
	# resize
	#win32gui.MoveWindow(hwnd, 0, 0, 500, 500, True)
	
time.sleep(3)
getFore()