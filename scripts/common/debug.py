#!c:\python25\python.exe


import datetime
import os
import traceback
import sys


# Program Imports
# ===============
sys.path.append("./common")
from common import *


###############################################################################
class Debug ():
###############################################################################


	if isWin():
		logfolder="C:\NewHomeControl\Scripts\logs"
	else:
		logfolder="/root/hc/scripts/logs"
		
	logfile=logfolder+"/log.txt"


	###############################################################################
	#def __init__ (self):
	###############################################################################
	#
	#
	#
	###############################################################################
	#	print "======================="
	#	print "Debug Class Constructor"
	#	print "======================="
	




	###############################################################################
	def Info(self, msg):
	###############################################################################
		
		now = datetime.datetime.now()
		timestamp=str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)
		msg = "["+str(timestamp)+"] - ["+str(msg)+"]"
		
		f = open(Debug.logfile, 'a+')
		f.write(msg+"\n")
		f.close()
			
		print msg
		
	
	###############################################################################
	def Info1(self, msg):
	###############################################################################
			
		x=0
		x=x+1
		#Debug.Info(self, "WARNING: " + msg)
	
	
	
	
	###############################################################################
	def Warning(self, msg):
	###############################################################################
		
		Debug.Info(self, "WARNING: " + msg)
					
	
	
	###############################################################################
	def Error(self, msg):
	###############################################################################
		
		Debug.Info(self, "= ERROR =============================================================")
		Debug.Info(self, msg)
		Debug.Info(self, "=====================================================================")
			

	###############################################################################
	def Exception(self, msg):
	###############################################################################

		print " "
		print " "		
		Debug.Info(self, "= EXCEPTION==========================================================")
		Debug.Info(self, msg)
		Debug.Info(self, "---------------------------------------------------------------------")
		print " "
		traceback.print_exc()
		print " "
		Debug.Info(self, "=====================================================================")
		print " "
		print " "
		


	###############################################################################
	def BackupLogfile(self):
	###############################################################################
	#
	#
	###############################################################################

		Debug.Info (self, "+++ backup_logfile +++")
		
		if os.path.exists(Debug.logfile):

			try:
				Debug.Info (self, "    Log file exists")

				now = datetime.datetime.now()
				d = now.date()
				t = now.time()
				Debug.Info (self, "    Datestamp Created")

				filename=Debug.logfolder+"\log-"+str(d.year)+"-"+str(d.month)+"-"+str(d.day)+"-"+str(t.hour)+"-"+str(t.minute)+"-"+str(t.second)+".txt"
				
				Debug.Info (self, "    Moving to ["+str(filename)+"]")
				os.rename(Debug.logfile, filename)
				Debug.Info (self, "    Done")
				
			except:
				Debug.Info (self, "EXCEPTION - Problem in backing up log file")

		Debug.Info (self, "--- backup_logfile ---")

	
	
	
	
	
	


		
	###############################################################################
	#def __del__ (self):
	###############################################################################
	#
	#
	#
	###############################################################################
	#	print "======================"
	#	print "Debug Class Destructor"
	#	print "======================"
		