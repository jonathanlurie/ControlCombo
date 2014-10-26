# performs a screen
# requires PIL and wxPython

import wx  # for accessing environment
from time import gmtime, strftime  # to access current time (to create unique file name)



def takeScreenshot():

	app = wx.App()  # Need to create an App instance before doing anything

	screen = wx.ScreenDC()	
	size = screen.GetSize()
	bmp = wx.EmptyBitmap(size[0], size[1])
	mem = wx.MemoryDC(bmp)
	mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
	del mem  # Release bitmap
	
	filename = strftime("%Y%m%d_%Hh%Mm%Ss", gmtime()) + "_sceenshot.png"
	bmp.SaveFile(filename, wx.BITMAP_TYPE_PNG)
	print("INFO: new screenshot at " + filename + ".")
