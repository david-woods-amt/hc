#!c:\python27\python.exe



import os
import sys
from _winreg import OpenKey, CloseKey, ConnectRegistry, HKEY_LOCAL_MACHINE, EnumValue
import wmi				## See http://msdn.microsoft.com/en-us/library/aa394074(v=vs.85).aspx



sys.path.append("./common")
from debug import *



###################################################################################
class Winstuff ():
###################################################################################

	

	###############################################################################
	# 
	#							Private Methods
	#
	###############################################################################
	# 
	#
	###############################################################################
		
	
	

	

	###############################################################################
	#def __init__ (self):
	###############################################################################
	#
	#
	#
	###############################################################################
	#	print "=========================="
	#	print "Winstuff Class Constructor"
	#	print "=========================="
	



		
	###############################################################################
	#def __del__ (self):
	###############################################################################
	#
	#
	#
	###############################################################################
	#	print "========================="
	#	print "Winstuff Class Destructor"
	#	print "========================="








	###############################################################################
	# 
	#							Public Methods
	#
	###############################################################################
	# 
	#
	###############################################################################
	



	###############################################################################
	def scan(self, searchfor):
	###############################################################################
	# Search the Windows Registry for the COM Port value
	#
	# Returns: 	Port Number if found
	#			0 if not found
	#
	###############################################################################

		port = 0

		debug=Debug()

		debug.Info ("+++ scan +++")
		debug.Info ("    Looking for ["+str(searchfor)+"]")

		# Look in Registry for COM Ports
		# ==============================
		try:
			aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
			debug.Info ("    Connected to Registry")

			aKey = OpenKey(aReg, r"Hardware\DEVICEMAP\SERIALCOMM")
			debug.Info ("    Read key")
			for i in range(1024):                                           
				try:
					name,value,t = EnumValue(aKey,i)

					if searchfor in name:
						port = value
						port=port.replace("COM", "")
						print "Found [" + searchfor + "] on Port ["+str(port)+"]"
						#print i, name, value, t
				except EnvironmentError:                                               
					#print "End of list"
					break          
			CloseKey(aKey) 
			CloseKey(aReg)
		except:
			debug.Exception ("Problem in searching for port ["+str(searchfor)+"]")


		debug.Info ("--- scan ---")
		return int(port)



	###############################################################################
	def getLaptopPower(self):
	###############################################################################
	# Read the power condition of the Laptop
	#
	###############################################################################

		debug=Debug()
		debug.Info1("+++ getLaptopPower +++")

		text=""

		c = wmi.WMI ()
		for battery in c.Win32_Battery ():

			if (battery.BatteryStatus == 1):	
				text = "The battery is discharging"
			elif (battery.BatteryStatus == 2):
				text = "Mains Powered"
			elif (battery.BatteryStatus == 3):
				text =  "Fully Charged"
			elif (battery.BatteryStatus == 4):
				text =  "Low"
			elif (battery.BatteryStatus == 5):
				text =  "Critical"
			elif (battery.BatteryStatus == 6):
				text =  "Charging"
			elif (battery.BatteryStatus == 7):
				text =  "Charging and High"
			elif (battery.BatteryStatus == 8):
				text =  "Charging and Low"
			elif (battery.BatteryStatus == 9):
				text =  "Charging and Critical"
			elif (battery.BatteryStatus == 10):
				text =  "Undefined"
			elif (battery.BatteryStatus == 11):
				text =  "Partially Charged"

		debug.Info1("--- getLaptopPower ---")

		return battery.BatteryStatus, battery.EstimatedChargeRemaining, text



		