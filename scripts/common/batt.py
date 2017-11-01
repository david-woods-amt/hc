import wmi

## See http://msdn.microsoft.com/en-us/library/aa394074(v=vs.85).aspx


c = wmi.WMI ()
for battery in c.Win32_Battery ():
	
	print "Charge Left ["+str(battery.EstimatedChargeRemaining)+"] %" 
	
	if (battery.BatteryStatus == 1):	
		print "The battery is discharging."
	elif (battery.BatteryStatus == 2):
		print "The system has access to AC."
	elif (battery.BatteryStatus == 3):
		print "Fully Charged"
	elif (battery.BatteryStatus == 4):
		print "Low"
	elif (battery.BatteryStatus == 5):
		print "Critical"
	elif (battery.BatteryStatus == 6):
		print "Charging"
	elif (battery.BatteryStatus == 7):
		print "Charging and High"
	elif (battery.BatteryStatus == 8):
		print "Charging and Low"
	elif (battery.BatteryStatus == 9):
		print "Charging and Critical"
	elif (battery.BatteryStatus == 10):
		print "Undefined"
	elif (battery.BatteryStatus == 11):
		print "Partially Charged"
