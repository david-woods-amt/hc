#!c:\python25\python.exe


import datetime
import os
import sys
import pickle


sys.path.append("./common")
from debug import *
from common import *






###############################################################################
class Settings ():
###############################################################################

	
	if isWin():
		settingsfilename = "./settings.txt"
	else:
		settingsfilename = "/root/hc/settings.txt"
	

	###############################################################################
	#def __init__ (self):
	###############################################################################
	#
	#
	#
	###############################################################################
	#	print "=========================="
	#	print "Settings Class Constructor"
	#	print "=========================="
	

	
	###############################################################################
	def is_settings_file(self):
	###############################################################################
	# 
	#
	# Returns: 
	#
	###############################################################################
				
		debug=Debug()
		debug.Info ("+++ is_settings_file +++")
			
		if os.path.exists(self.settingsfilename):
			return 1
		else:
			return 0
		
		

	###############################################################################
	def save_settings(self, timerdata):
	###############################################################################
	# Saves settings to file
	#
	# Returns: Nothing
	#
	###############################################################################
			
		debug=Debug()
		debug.Info ("+++ save_settings +++")
	
		try:
			f = open(Settings.settingsfilename, 'wb')
			pickle.dump(timerdata, f)
			f.close()
	
		except Exception, e:
			debug.Exception ("Problem in saving settings. ["+str(e)+"]")
	
		debug.Info ("--- save_settings ---")
	
	
	
	
	
	###############################################################################
	def read_settings(self):
	###############################################################################
	# Reads settings from file into the timerdata global
	#
	# Returns: Nothing
	#
	###############################################################################
	
		debug=Debug()
				
		debug.Info ("+++ read_settings +++")
	
		try:
			f = open(Settings.settingsfilename, 'r')
			timerdata = pickle.load(f)
			f.close()
			debug.Info ("    Setting file read successfully")
	
		except Exception, e:
			debug.Exception ("Problem in reading settings. ["+str(e)+"]")
		
		debug.Info ("--- read_settings ---")
	
		return timerdata
	

	
	
	
	
	
	


		
	###############################################################################
	#def __del__ (self):
	###############################################################################
	#
	#
	#
	###############################################################################
	#	print "========================="
	#	print "Settings Class Destructor"
	#	print "========================="
		