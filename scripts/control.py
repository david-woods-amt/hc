#   !c:\python27\python.exe



###############################################################################
# Imports
###############################################################################


# Python Imports
# ==============
import os
import sys
import time
import datetime


# Program Imports
# ===============
sys.path.append("./common")

from common import *
from sock import *
###from phone import *
from settings import *
from zwave import *

if isWin():
	import msvcrt
else:
	from linuxstuff import *

###############################################################################
# Constants
###############################################################################

# Mobile Phone Globals
# ====================
#sender = "+447919404812"
#sender1 = "+447711626311"


# Timer Array Constants
# =====================
NUMBEROFZWAVEDEVICES=11
HEATING=0

LIGHT1=1
LIGHT2=2
LIGHT3=3
LIGHT4=4
LIGHT5=5

SOCKET1=6
SOCKET2=7
SOCKET3=8
SOCKET4=9
SOCKET5=10

# Laptop Battery
# ==============
batteryAlarmCutoff=55		# At what % of power left do we alarm
batteryAlarmInterval=3600	# How many seconds between Alarm messages


###############################################################################
# Globals
###############################################################################

# Laptop Globals
# ==============
batteryValue=0
batteryCharge=0
batteryText=""
batteryAlarm=0
batteryAlarmIntervalStart=0
batteryAlarmIntervalEnd=0


# Mobile Phone Globals
# ====================
#phone=False
#phone_responding=False
#imei=""
#batt=""
#signal=""


# General Globals
# ===============
t=None
#zwave.isResponding()=False
#zwave=False
#atHome=True

# Alarms and Status
# =================
dailystatussent=False
alarmmesagesent=False


# Create the data Structure for all ZWave Devices
# ===============================================
timerdata = []
for x in xrange(NUMBEROFZWAVEDEVICES):
	timerdata.append([])

	# Hours of the Day
	for y in xrange(7):
		timerdata[x].append([])
						#0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7  
		timerdata[x][y]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

	
	# Other Variables
	timerdata[x].append("Name")				# Name
	timerdata[x].append(0)					# Power
	timerdata[x].append(0)					# Timer
	timerdata[x].append(0)					# Boost
	timerdata[x].append(0)					# BoostStartTime
	timerdata[x].append(0)					# BoostElapsedTime
	timerdata[x].append(0)					# BoostLength
	timerdata[x].append(0)					# OnOff
	timerdata[x].append(0)					# OldOnOff
	timerdata[x].append(0)					# Dimmer Control
	timerdata[x].append(0)					# ZWavePort
	timerdata[x].append(0)					# ZWaveType - Heating, Light, Socket


# Pointers into the "timerdata" array
# ===================================
NAME=7
POWER=8
TIMER=9
BOOST=10
BOOSTSTARTTIME=11
BOOSTELAPSEDTIME=12
BOOSTLENGTH=13
STATE=14
OLDSTATE=15
#DIMMERCONTROL=16
ZWAVEPORT=17
ZWAVETYPE=18


# DEBUG
for x in xrange(NUMBEROFZWAVEDEVICES):
	timerdata[x][7]=0
	timerdata[x][8]=0
	timerdata[x][9]=0
	timerdata[x][10]=0
	timerdata[x][11]=0
	timerdata[x][12]=0
	timerdata[x][13]=0
	timerdata[x][14]=0
	timerdata[x][15]=0
	timerdata[x][16]=0
	timerdata[x][17]=0
	timerdata[x][18]=0
	



# Set up some specific Data Values
# ================================
timerdata[HEATING][NAME]="Central Heating"
timerdata[HEATING][BOOSTLENGTH]=15 #3600
timerdata[HEATING][ZWAVEPORT]="\x03"
timerdata[HEATING][ZWAVETYPE]="HEATING"

timerdata[LIGHT1][NAME]="Main Bedroom Light"
timerdata[LIGHT1][ZWAVEPORT]="\x02"
timerdata[LIGHT1][ZWAVETYPE]="LIGHT"

timerdata[LIGHT2][NAME]="Spare Bedroom Light"
timerdata[LIGHT2][ZWAVEPORT]="\x06"
timerdata[LIGHT2][ZWAVETYPE]="LIGHT"

timerdata[LIGHT3][NAME]="Sitting Room Light"
timerdata[LIGHT3][ZWAVEPORT]="\x06"
timerdata[LIGHT3][ZWAVETYPE]="LIGHT"

timerdata[LIGHT4][NAME]="Dining Room Light"
timerdata[LIGHT4][ZWAVEPORT]="\x06"
timerdata[LIGHT4][ZWAVETYPE]="LIGHT"

timerdata[LIGHT5][NAME]="Kitchen Light"
timerdata[LIGHT5][ZWAVEPORT]="\x07"
timerdata[LIGHT5][ZWAVETYPE]="LIGHT"

timerdata[SOCKET1][NAME]="Main Bedroom Socket"
timerdata[SOCKET1][ZWAVEPORT]="\x06"
timerdata[SOCKET1][ZWAVETYPE]="SOCKET"

timerdata[SOCKET2][NAME]="Spare Bedroom Socket"
timerdata[SOCKET2][ZWAVEPORT]="\x06"
timerdata[SOCKET2][ZWAVETYPE]="SOCKET"

timerdata[SOCKET3][NAME]="Sitting Room Socket"
timerdata[SOCKET3][ZWAVEPORT]="\x06"
timerdata[SOCKET3][ZWAVETYPE]="SOCKET"

timerdata[SOCKET4][NAME]="Dining Room Socket"
timerdata[SOCKET4][ZWAVEPORT]="\x06"
timerdata[SOCKET4][ZWAVETYPE]="SOCKET"

timerdata[SOCKET5][NAME]="Kitchen Socket"
timerdata[SOCKET5][ZWAVEPORT]="\x07"
timerdata[SOCKET5][ZWAVETYPE]="SOCKET"





###############################################################################
def routine_check_on_zwave():
###############################################################################
# Do a routine check on the Z Wave devices
#
# Sets global zwave variables
#
###############################################################################
	
	global zwave
	global timerdata
	global t
	
	debug=Debug()
	debug.Info1("+++	routine_check_on_zwave +++")
		
	if zwave.isActive() == True:
		if (t.second==45):
			debug.Info("Scheduled check on ZWave")

			(timerdata[HEATING][STATE],error) = zwave.get_node(timerdata[HEATING][ZWAVEPORT], timerdata[HEATING][ZWAVETYPE])
		
	debug.Info1("---	routine_check_on_zwave ---")	
		







###############################################################################
#def routine_check_on_phone():
###############################################################################
#
#
#
###############################################################################
#
#	global phone
#	global t
#	
#	debug=Debug()
#	debug.Info1("+++	routine_check_on_phone +++")
#	
#	if phone.isActive() == True:
#		if (t.second==15):
#			debug.Info("Scheduled Check on Phone")
#
#			(batt,error) = phone.get_battery()
#			#(signal,error) = phone.get_signal()
#			#(imei,error) = phone.get_imei()
#			
#			#debug.Info("IMEI ["+str(imei)+"] - Battery ["+str(batt)+"] - Signal ["+str(signal)+"]")
#			debug.Info ("Battery ["+str(batt)+"]")
#	
#	debug.Info1("--- routine_check_on_phone ---")
#		




###############################################################################
def process_keyboard_command(key):
###############################################################################
#
#
#
###############################################################################

	# ======================
	# Keyboard Heating Debug 
	# ======================
	if key:
		print "Key hit ["+key+"]"
	
		key = str(key)
		key=key.upper()

		if (key=='P'):
			process_commands('POWER-HEATING-0',0)
		if (key=='B'):
			process_commands('BOOST-HEATING-0',0)
		if (key=='T'):
			process_commands('TIMER-HEATING-0',0)
		if (key=='S'):
			process_commands('STATUS-ALL-1',0)
		if (key=='Z'):
			check_to_restart_zwave(1)
						
			
		if (key=='Q'):
			sys.exit(1)
			






###############################################################################
#def check_to_restart_phone():
###############################################################################
#
#
#
###############################################################################
#
#	global phone
#	global t
#	
#	debug=Debug()
#	debug.Info1("+++	check_to_restart_phone +++")
#	
#	# If no Phone, restart serial port
#	# ======================================
#	if phone.isActive() == False:
#		if (t.second==5):
#			debug.Info("Trying to restart phone")
#			time.sleep(1)
#			phone.init_phone()
#			if phone.isResponding()==True:
#				debug.Info("Restarted OK")
#			else:
#				debug.Info("Failed to restart")
#
#	debug.Info1("---	check_to_restart_phone ---")
#















###############################################################################
def check_to_restart_zwave(key=0):
###############################################################################
#
# Pass in a Key to force a check
# 
###############################################################################

	global zwave
	global t
	
	debug=Debug()
	debug.Info1("+++ check_to_restart_zwave +++")
	
	# No Z-Wave, restart serial port
	if zwave.isActive()==False:
		if (t.second==35) | (key==1):
			debug.Info("Trying to restart zwave")
			time.sleep(1)
			zwave.init_zwave()
			if zwave.isResponding() == True:
				debug.Info("Restarted OK")
			else:
				debug.Info("Failed to restart")


	debug.Info1("--- check_to_restart_zwave ---")
	
	

###############################################################################
def check_laptop_power():		
###############################################################################
#
#
#
###############################################################################

	global batteryValue
	global batteryCharge
	global batteryText
	global batteryAlarm
	global batteryAlarmCutoff
	
	global winstuff
	
	debug=Debug()
	debug.Info1("+++ check_laptop_power +++")
	
	# Check on Laptop Power
	# ======================
	(batteryValue, batteryCharge, batteryText)=winstuff.getLaptopPower()
	if batteryCharge < batteryAlarmCutoff:
		batteryAlarm=1
	else:
		batteryAlarm=0

	debug.Info1("--- check_laptop_power ---")
	


	
###############################################################################
def format_status(value, format):
###############################################################################
# Provide HTML formatted string for heating 
#
# Returns html formatted string
###############################################################################

	debug=Debug()
	debug.Info1("+++ format_status +++")
	debug.Info1("    Value is  ["+str(value)+"]")
	debug.Info1("    Format is ["+str(format)+"]")
	
	status=""
	
	if value==0:
		status="Off"
	elif value==1:
		status="On"
	#else:
		#status="UNKNOWN"	
	
	if format == "html":
		if value==0:
			status = "<font color=\"red\"><b>Off</b></font>"
		elif value==1:
			status = "<font color=\"green\"><b>On</b></font>"
		else:
			status = "<font color=\"green\"><b>"+str(value)+"%</b></font>"
	
	
	debug.Info1("    Returning ["+str(status)+"]")
	debug.Info1("--- format_status ---")
	
	return status


###############################################################################
def button (page, function, command, label, name):
###############################################################################
# Returns a string that creates a button with all the required data
#
#
#
###############################################################################

	debug=Debug()
	debug.Info1("+++ button +++")
	
	line = "\n\n"
	
	line += "<form id='sampleform' method='get' action='"+page+"?request="+command+"'>\n"
##	line += "	<input type='hidden' name='type' value='"+function+"'>\n"
	line += "	<input type='hidden' name='command' value='"+command+"'>\n"
	line += "	<input type='submit' class='button' name='Submit' value='"+label+"'\n"
	

	if name == "Disabled":
		line += "Disabled=\"Disabled\""
	line += "/>\n"
	
	if name != "":
		line += "	<input type='hidden' name='name' value='"+name+"' />\n"
		
	line += "</form>\n\n\n"
	
	debug.Info1("--- button ---")
	
	return line
			

###############################################################################
#def status_string_sms():
###############################################################################
# Create general status string
#
# Returns SMS formatted status string
#
###############################################################################
#
#	global zwave
#	global phone
#	global sock
#	global timerdata
#
#	debug=Debug()
#	debug.Info("+++ status_string_sms +++")
#
#	cmd = ""
#		
#	# Get the time of day
#	cmd += time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()) + " "
#		
#	# ERRORS and WARNINGS
#	# ===================
#	if zwave.isActive() == False:
#		cmd += "ERROR: Z-Wave not Active! "
#	if phone.isActive() == False:
#		cmd += "ERROR: Phone not Active! "
#	if zwave.isResponding() == False:
#		cmd += "WARNING: Z-Wave is not responding! "
#	if phone.isResponding() == False:
#		cmd += "WARNING: Phone is not responding! "
#
#
#	for device in xrange(NUMBEROFZWAVEDEVICES):
#		cmd += timerdata[device][NAME].upper()+" "
#		cmd += "Power["+format_status(timerdata[device][POWER],"")+"] "
#		cmd += "Timer["+format_status(timerdata[device][TIMER],"")+"] "
#		cmd += "Boost["+format_status(timerdata[device][BOOST],"")+"] "
#		cmd += "State["+format_status(timerdata[device][STATE],"")+"] "
#
#
#	addr=sock.get_ip_address()
#	if addr:
#		cmd += str(" Server Address is http://"+addr+"/hc/index.jsp")
#						
#	debug.Info("--- status_string_sms ---")
#	return cmd
#	
	
	
	
	


###############################################################################
def status_string(what, format):
###############################################################################
# Create general status string
#
# Returns HTML/Email formatted status string
#
###############################################################################

	global zwave
#	global phone
	global sock
	global winstuff
	global timerdata
	
	global batteryAlarm

	debug=Debug()
	debug.Info("+++ status_string +++")
	debug.Info("    Status of         ["+what+"]")
	
	try:
	
		cmd = ""
		# Get the time of day
#		cmd += time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()) + "<p> "
		
		# ERRORS and WARNINGS
		# ===================
		if format=="html":
			cmd += "<article>"
		if zwave.isActive() == False:
			cmd += "<b>ERROR: Z-Wave is not working correctly...cannot action heating! </b><br>"
###		if phone.isActive() == False:
###			cmd += "<b>ERROR: Phone is not working correctly...cannot process SMS! </b><br>"
		if zwave.isResponding() == False:
			cmd += "<b>WARNING: Z-Wave is not responding...cannot action heating! </b><br>"
###		if phone.isResponding() == False:
###			cmd += "<b>WARNING: Phone is not responding...cannot process SMS! </b><br>"
		if format=="html":
			cmd += "</article>"

		
		# Gather Status for ALL Heating ZWAVE Devices
		# ===========================================
		#
		if (what == "ALL") or (what == "HEATING"):

			#cmd += "<hr>"
			if format=="html":
				cmd += "<h2>Heating</h2>\n"
			
			if (what != "ALL"):
				if format=="html":
					#cmd+=button("main.cgi", "heating", "STATUS-HEATING-ALL", "Update Heating Status", "")
					cmd+=button("main.cgi", "heating", "STATUS-ALL-1", "Update All Status", "")
			
			cmd += "<table id=\"results\" >\n"
			cmd += "<tr> <th>Area</th> <th>Power</th> <th>Timer</th>  <th>Boost</th> <th>State</th>"
			if (what != "ALL"):
				cmd += "<th colspan=\"5\">Controls </th>"
			cmd += "</tr>\n"
			
			for device in xrange(NUMBEROFZWAVEDEVICES):

				if timerdata[device][ZWAVETYPE]=="HEATING":
					cmd += "<tr>"
					cmd += "<td>"+timerdata[device][NAME]+"</td>"
					cmd += "<td>"+format_status(timerdata[device][POWER],format)+"</td>"
					cmd += "<td>"+format_status(timerdata[device][TIMER],format)+"</td>"
					cmd += "<td>"+format_status(timerdata[device][BOOST],format)+"</td>"
					

					
					if timerdata[device][BOOST] == 1:
						x = timerdata[device][BOOSTLENGTH] - timerdata[device][BOOSTELAPSEDTIME]
						x=round(x, 1)
						if x > 60:
							x=x/60
							x=round(x, 1)
							cmd += "<td>Boost Remaining ["+str(x)+"] (minutes)</td>"
						else:
							cmd += "<td>Boost Remaining ["+str(x)+"] (seconds)</td>"
						
						
					# Do an actual read
					(timerdata[device][STATE],error) = zwave.get_node(timerdata[device][ZWAVEPORT], timerdata[device][ZWAVETYPE])

					if zwave.isActive()!=True or zwave.isResponding()!=True:
						cmd += "<td>State[UNKNOWN]</td>"
					else:
						cmd += "<td>State["+format_status(timerdata[device][STATE],format)+"]</td>"
					
					
					if format=="html":
						if (what != "ALL"):
							#cmd += "<table width = \"100%\"><tr><td>"
							cmd += "<td>"

							# Power Button
							# ============
							if timerdata[device][POWER]==1:
								disabled=""
							else:
								disabled="Disabled"
							cmd += button("main.cgi", "heating", "POWER-HEATING-"+str(device), "Power Off", disabled)
							cmd += "</td><td>"						

							# Timer Button
							# ============
							if timerdata[device][TIMER]==0:
								label="On"
							else:
								label="Off"
							cmd += button("main.cgi", "heating", "TIMER-HEATING-"+str(device), "Timer "+label, "")
							cmd += "</td><td>"				

							# Boost Button
							# ============
							if timerdata[device][BOOST]==0:
								label="On"
							else:
								label="Off"
							cmd += button("main.cgi", "heating", "BOOST-HEATING-"+str(device), "Boost "+label, "")

							# Get Timer Button
							# ================
							cmd += "</td><td>"
							cmd += button("main.cgi", "heating", "GETTIMES-HEATING-"+str(device), "Get Timer Values", timerdata[device][NAME] )
							
							
							# Get Boost Button
							# ================
							cmd += "</td><td>"
							cmd += button("main.cgi", "heating", "GETBOOST-HEATING-"+str(device), "Get Boost Value", timerdata[device][NAME] )
							
							
							#cmd += "</td></tr></table>"
					cmd += "</tr>"
					
			if format=="html":
				cmd += "</table>"

	
			
		# Gather Status for ALL Lighting ZWAVE Devices
		# ============================================
		if (what == "ALL") or (what == "LIGHT"):
		
			if format=="html":
				cmd += "<h2>Lights</h2>\n"
				
				if (what != "ALL"):
					cmd+=button("main.cgi", "light", "STATUS-LIGHT-ALL", "Update Light Status", "")
			
				cmd += "<table id=\"results\" >\n"
				cmd += "<tr> <th>Area</th> <th>Power</th> <th>Timer</th>  <th>State</th>"
				if (what != "ALL"):
					cmd += "<th colspan=\"5\">Controls </th>"
				cmd += "</tr>\n"
				
			
			for device in xrange(NUMBEROFZWAVEDEVICES):

				if timerdata[device][ZWAVETYPE]=="LIGHT":
					
					# Do an actual read
					(timerdata[device][STATE],error) = zwave.get_node(timerdata[device][ZWAVEPORT], timerdata[device][ZWAVETYPE])
					
					# As Dimmers take a while to react, maybe tweak the power setting
					if timerdata[device][STATE]>0:
						timerdata[device][POWER]=1
					else:
						timerdata[device][POWER]=0
					
					cmd += "<tr>"
					cmd += "<td>"+timerdata[device][NAME]+"</td>"
					cmd += "<td>"+format_status(timerdata[device][POWER],format)+"</td>"
					cmd += "<td>"+format_status(timerdata[device][TIMER],format)+"</td>"
					#cmd += " Dimmer Control["+format_status(timerdata[device][DIMMERCONTROL],format)+"]"
								
					if zwave.isActive()!=True or zwave.isResponding()!=True:
						cmd += "<td>[UNKNOWN]</td>"
					else:
						cmd += "<td>"+format_status(timerdata[device][STATE],format)+"</td>"		
					
									
					if format=="html":
						if (what != "ALL"):
							
							# Power Button
							# ============
							if timerdata[device][POWER]==1:
								disabled=""
							else:
								disabled="Disabled"
							cmd += "<td>"+button("main.cgi", "light", "POWER-LIGHT-"+str(device), "Power Off", disabled)+"</td>"
							
							# Timer Button
							# ============
							if timerdata[device][TIMER]==0:
								label="On"
							else:
								label="Off"
							cmd += "<td>"+button("main.cgi", "light", "TIMER-LIGHT-"+str(device), "Timer "+label, "")+"</td>"
							
							# Dimmer Button
							# =============
							cmd += "<td>"+button("main.cgi", "light", "DIMMERUP-LIGHT-"+str(device), "Dimmer Up", "")+"</td>"
							cmd += "<td>"+button("main.cgi", "light", "DIMMERDOWN-LIGHT-"+str(device), "Dimmer Down", "")+"</td>"
							
							# Get Times Button
							# ================
							cmd += "<td>"+button("timer.jsp", "light", "GETTIMES-LIGHT-"+str(device), "Get Timer Values", timerdata[device][NAME] )+"</td>"
							
							cmd += "</tr>"
							
			cmd += "</table>"
					
					
			
		
			
		# Gather Status for ALL Socket ZWAVE Devices
		# ==========================================
		if (what == "ALL") or (what == "SOCKET"):
		
			#cmd += "<hr>"
			if format=="html":
				cmd += "<h2>Sockets</h2>\n"
				
			if format=="html":
				if (what != "ALL"):
					cmd+=button("main.cgi", "socket", "STATUS-SOCKET-ALL", "Update Socket Status", "")
			
			cmd += "<table id=\"results\" >\n"
			cmd += "<tr> <th>Area</th> <th>Power</th> <th>Timer</th>  <th>State</th>"
			if (what != "ALL"):
				cmd += "<th colspan=\"5\">Controls </th>"
			cmd += "</tr>\n"
							
			for device in xrange(NUMBEROFZWAVEDEVICES):
		
				if timerdata[device][ZWAVETYPE]=="SOCKET":
					cmd += "<td>"+timerdata[device][NAME]+"</td>"
					cmd += "<td>"+format_status(timerdata[device][POWER],format)+"</td>"
					cmd += "<td>"+format_status(timerdata[device][TIMER],format)+"</td>"
			
					# Do an actual read
					(timerdata[device][STATE],error) = zwave.get_node(timerdata[device][ZWAVEPORT], timerdata[device][ZWAVETYPE])
					
					if zwave.isActive()!=True or zwave.isResponding()!=True:
						cmd += "<td>State[UNKNOWN]</td>"
					else:
						cmd += "<td>State["+format_status(timerdata[device][STATE],format)+"</td>"
					
					
					
					if format=="html":
						if (what != "ALL"):
							cmd += "<td>"+button("main.cgi", "socket", "POWER-SOCKET-"+str(device), "Power", "")+"</td>"
							cmd += "<td>"+button("main.cgi", "socket", "TIMER-SOCKET-"+str(device), "Timer", "")+"</td>"
							cmd += "<td>"+button("timer.jsp", "socket", "GETTIMES-SOCKET-"+str(device), "Get Timer Values", timerdata[device][NAME] )+"</td>"
				cmd += "</tr>"
			
			if format=="html":
				cmd += "</table>"
			
		
#		if what == "ALL":
#			(batteryValue, batteryCharge, batteryText)=winstuff.getLaptopPower()
#			if format=="html":
#				cmd += "<hr>"
#				if batteryCharge < batteryAlarmCutoff:
#					cmd += "<font color=\"red\"><b>Laptop Charge is ["+str(batteryCharge)+"]%</b></font><br>"
#				else:
#					cmd += "Laptop Charge is ["+str(batteryCharge)+"]%<br>"
#
#				cmd += "Laptop Status is ["+str(batteryText)+"]<br>"
#				cmd += "Laptop Alarm is ["+str(batteryAlarm)+"]"
#			else:
#				cmd += " Laptop Charge is ["+str(batteryCharge)+"]%."

		
#		if what == "ALL":
#			if (format=="email"):
#				addr=sock.get_ip_address()
#				if addr:
#					if format=="html" or format=="email":
#						cmd += "<hr>"
#						cmd += str("<p><a href=\"http://"+addr+"/hc/index.jsp\"> Server Address is http://"+addr+"/hc/index.jsp</a>")
#					else:
#						cmd += str(" Server Address is http://"+addr+"/hc/index.jsp")
#


	except Exception, e:
		debug.Exception("Problem in creating status string. ["+str(e)+"]")
	
	
	debug.Info("--- status_string ---")
	
	cmd="Content-type: text/html\n\n<!DOCTYPE html><html><head><title>My first Python CGI app</title></head><body>"+cmd+"</body></html>"
	return cmd
	
		
		
###############################################################################
def process_any_socket_commands():
###############################################################################
#
#
#
###############################################################################
		
	global zwave
#	global phone
	global sock
	global winstuff
	global settings
	global timerdata
	
	debug=Debug()
		

	# Check for a socket write from Website
	# =====================================
	try:
		
			(channel, data) = sock.readsocket()
		
			#debug.Info(data)
			
			#if data.find("BOOST") != -1:
			#	data="BOOST-HEATING-0"
			data = data.replace('POST / HTTP/1.1', '', 1)
			data = data.replace('\n', '', 2)
			data = data.replace('\r', '', 2)
			
#			debug.Info(data)
			
			if data:
				debug.Info("Data is ["+str(data)+"]")

				if data.startswith("WATCHDOG"):
					debug.Info("Watchdog Check")
					status="All OK"

				
				elif data.startswith("EMAIL-ADMIN-ALL"):
					debug.Info("Email Status Request for ["+data+"]")
					status = status_string("ALL", "email")
					sock.send_email(status)
				
				elif data.startswith("STATUS"):
					debug.Info("Status Request for ["+data+"]")
					process_commands(data, 0)
					(command, product, node) = data.split("-")
					status = status_string(product, "html")


				elif (data.startswith("POWER")) or (data.startswith("TIMER")) or (data.startswith("BOOST")):
					debug.Info("Request for ["+data+"]")
					process_commands(data, 0)
					(command, product, node) = data.split("-")
					status = status_string(product, "html")


				elif data.startswith("SETTIMES"):
					status=set_timer_data(data)
					settings.save_settings(timerdata)


				elif data.startswith("GETTIMES"):
					status=get_timer_data(data)
					status="Content-type: text/html\n\n"+status
				
				
				
				elif data.startswith("GETBOOST"):
					status=get_boost_data(data)
					status="Content-type: text/html\n\n"+status
				
				elif data.startswith("SETBOOST"):
					status=set_boost_data(data)
					status="Content-type: text/html\n\n"+status
					settings.save_settings(timerdata)



				elif (data.startswith("DIMMERUP-LIGHT")):
					debug.Info("Request for ["+data+"]")
					process_commands(data, 0)
					(command, product, node) = data.split("-")
					status = status_string(product, "html")


				elif (data.startswith("DIMMERDOWN-LIGHT")):
					debug.Info("Request for ["+data+"]")
					process_commands(data, 0)
					(command, product, node) = data.split("-")
					status = status_string(product, "html")


				else:
					# Send back the status
					status = "Unknown Command ["+data+"]"

				
				channel.send('HTTP/1.0 200 OK\n')
				channel.send(status)
				#print " ========================== Data is ["+str(status)+"] ========================="
				channel.close() # disconnect
	
	except Exception, e:
		debug.Exception("Problem in socket reading. ["+str(e)+"]")



###############################################################################
def set_timer_data(blob):
###############################################################################
# Sets up the Heating data in response from Web Server Post
#
# Returns "Done"
#
###############################################################################

	global timerdata
	
	debug.Info("+++ set_timer_data for object ["+blob+"] +++")
		
	try:
		status = ""

		(cmd, function, device, data) = blob.split("-")
		
		debug.Info("  Command ["+str(cmd)+"]")
		debug.Info("  Function ["+str(function)+"]")
		debug.Info("  Device ["+str(device)+"]")
		debug.Info("  Data ["+str(data)+"] ")
		device=int(device)

		# Clear timer data
		for x in range(0, 7):	
			for y in range(0, 48):
				timerdata[device][x][y] = 0
	
		items = data.split(",")
		
		debug.Info("    Items are ["+str(items)+"]")

		for item in items:
			debug.Info("    Item is ["+str(item)+"]")
			times = item.split("&")

#			if item != "":
#				if times:
			if item.find("=") == -1:
#				debug.Info("    URL End")
#			else:
				
				x = times[0]
				y = times[1]
					
				x = int(x, 10)
				y = int(y, 10)
					
				debug.Info("    Times for Device ["+str(device)+"] is ["+str(times)+"]" )

				timerdata[device][x][y] = 1
				status="OK"
			else:
				debug.Info("    URL End")
		
		#print timerdata[device]
		
	except Exception, e:
		debug.Info("EXCEPTION: Problem in set_timer_data. ["+str(e)+"]")
		status = "ERROR"
	
	status = "Done"
	debug.Info("--- set_timer_data ---")
	return status
	

###############################################################################
def get_timer_data(blob):
###############################################################################	
# Gets heating timer data in response to a web site request
#
# Returns timer data
#
###############################################################################

	global timerdata

	debug.Info("+++ get_timer_data for object ["+blob+"] +++")
	
	try:	
		(cmd, function, device) = blob.split("-")
		debug.Info("Command ["+str(cmd)+"] - Function ["+str(function)+"] - Device ["+str(device)+"] - Data ["+str(blob)+"] ")
		
		device=int(device)
		data = "GETTIMES-HEATING-"+str(device)+"="
		data = header = table = footer = ""

		for x in range(0, 7):	
			for y in range(0, 48):
				if timerdata[device][x][y] == 1:
					data += str(x)+"&"+str(y)+","


		#print timerdata[device]
		print "Data is ["+data+"]"
		
		#data=data+"Content-type: text/html\n\n"
		
		#header=header+"<form method=\"run\" action=\"main.cgi\">"
		#footer = "<input type=\"submit\" value=\"Submit\" name=\"B1\"> </form> </p>"
		#data=header+data+footer
		 
		

	except Exception, e:
		debug.Info("EXCEPTION: Problem in get_timer_data. ["+str(e)+"]")
		data = ""

	debug.Info("--- get_timer_data ---")
	
	return data





###############################################################################
def get_boost_data(blob):
###############################################################################	
# Gets boost data in response to a web site request
#
# Returns timer data
#
###############################################################################

	global timerdata

	debug.Info("+++ get_boost_data for object ["+blob+"] +++")
	
	try:	
		(cmd, function, device) = blob.split("-")
		debug.Info("Command ["+str(cmd)+"] - Function ["+str(function)+"] - Device ["+str(device)+"] - Data ["+str(blob)+"] ")
		
		device=int(device)
		data = "GETBOOST-HEATING-"+str(device)+"="+str(timerdata[device][BOOSTLENGTH])	# - timerdata[device][BOOSTELAPSEDTIME]
		
		print "Data is ["+data+"]"
		

	except Exception, e:
		debug.Info("EXCEPTION: Problem in get_boost_data. ["+str(e)+"]")
		data = ""

	debug.Info("--- get_boost_data ---")
	
	return data





###############################################################################
def set_boost_data(blob):
###############################################################################
# Sets the Boost value in response from Web Server Post
#
# Returns "Done"
#
###############################################################################

	global timerdata
	
	debug.Info("+++ set_boost_data for object ["+blob+"] +++")
		
	try:
		status = ""

		(cmd, function, device, data) = blob.split("-")
		
		debug.Info("Command ["+str(cmd)+"] - Function ["+str(function)+"] - Device ["+str(device)+"] - Data ["+str(data)+"] ")
		device=int(device)

		
		timerdata[device][BOOSTLENGTH] = int(data)
		
		
	except Exception, e:
		debug.Info("EXCEPTION: Problem in set_boost_data. ["+str(e)+"]")
		status = "ERROR"
	
	status = "Done"
	debug.Info("--- set_boost_data ---")
	return status
	
	
	
	
	


	

###############################################################################
def process_commands(data, needsms):
###############################################################################
# Process the commands
# 
# This is the core handler for all command. Handles the state logic 
#
# Returns	True if all OK
#			False if not OK
###############################################################################
	
	global timerdata
	global zwave
#	global phone
	
	
	debug=Debug()
	debug.Info("+++ process_commands +++")
	debug.Info("    Command is     ["+str(data)+"]")
	debug.Info("    Need SMS       ["+str(needsms)+"]")

		
	(cmd, product, node) = data.split("-")
	debug.Info("    Command is     ["+cmd+"]")
	debug.Info("    Product is     ["+product+"]")
	debug.Info("    Node is        ["+node+"]")
	
	if node!="ALL":
		node=int(node)
		
	ok = False
	
	try:

		if cmd!="STATUS":
			debug.Info("    Initial State  ["+str(timerdata[node][STATE])+"]")
	
			# Remeber old state to see if we need to send an update
			timerdata[node][OLDSTATE] = timerdata[node][STATE]
	
			# Do nothing if Z-Wave is not working
			# ===================================
			if zwave.isActive()==False or zwave.isResponding()==False:
			
				# Send a SMS if needed
				# ====================
#				if needsms==1:
#					msg = status_string_sms()
#					error = phone.send_sms_message(sender, msg)
#					#perror(error)
				
				debug.Info("--- process_commands (early from no ZWave) ---")
				return False
	
			else:
		
				if cmd=="POWER":
					debug.Info("Power Command")
	
					# If Power was ON, switch it all off
					if timerdata[node][POWER]==1:
						timerdata[node][POWER]=0
						timerdata[node][BOOST]=0
						timerdata[node][TIMER]=0
						timerdata[node][STATE]=0
					else:
						# Only if Timer, Power ON
						if timerdata[node][TIMER]==1:
							timerdata[node][POWER]=1
	
	
				if cmd=="BOOST":
					debug.Info("Boost Command")
	
					if timerdata[node][TIMER]==1 and timerdata[node][STATE]==1:
						debug.Info("Sorry: Boost command has no purpose here where Timer and Heating are on")
	
					# If Boost was ON, switch it off
					if timerdata[node][BOOST]==1:
						timerdata[node][BOOST]=0
#						timerdata[node][STATE]=0
						timerdata[node][BOOSTELAPSEDTIME]=0
						timerdata[node][BOOSTSTARTTIME]=0
					# Else Boost ON
					else:
						timerdata[node][STATE]=1
						timerdata[node][BOOST]=1
						timerdata[node][POWER]=1 	# implied
						timerdata[node][BOOSTSTARTTIME]=time.time()
	
				if cmd=="TIMER":
					debug.Info("Timer Command")
					debug.Info(str(timerdata))
	
					# If Timer was ON, switch it off
					if timerdata[node][TIMER]==1:
						timerdata[node][TIMER]=0
					# Else timer ON
					else:
						timerdata[node][TIMER]=1
						timerdata[node][POWER]=1 	# implied
	
				
				if cmd=="DIMMERUP":
					debug.Info("Dimmer UP Command")
					timerdata[node][TIMER]=0
				
					timerdata[node][STATE] = timerdata[node][STATE] + 25
					timerdata[node][POWER]=1
					if timerdata[node][STATE] > 99:
						timerdata[node][STATE]=99
					
					
				if cmd=="DIMMERDOWN":
					debug.Info("Dimmer DOWN Command")
					timerdata[node][TIMER]=0
					
								
					timerdata[node][STATE] = timerdata[node][STATE] - 25
					if timerdata[node][STATE] <= 0:
						timerdata[node][STATE]=0
						
						
				if cmd=="DIMMERSWITCH":
					debug.Info("Dimmer Switch Command")
					timerdata[node][TIMER]=0
				
				
				# Check the timer settings
				process_zwave_timers()


				# Sanity Check
				# ============
				for node in xrange(NUMBEROFZWAVEDEVICES):

					if timerdata[node][ZWAVETYPE]=="HEATING" and timerdata[node][BOOST]==0 and timerdata[node][TIMER]==0:
						timerdata[node][POWER]=0
						timerdata[node][STATE]=0
						timerdata[node][BOOSTELAPSEDTIME]=0
						timerdata[node][BOOSTSTARTTIME]=0

					if timerdata[node][ZWAVETYPE]=="HEATING" and timerdata[node][BOOST]==1:
						timerdata[node][POWER]=1

					if timerdata[node][TIMER]==1:
						timerdata[node][POWER]=1

					if timerdata[node][ZWAVETYPE]=="LIGHT" and timerdata[node][TIMER]==0 and timerdata[node][STATE]==0:
						timerdata[node][POWER]=0
					if timerdata[node][ZWAVETYPE]=="LIGHT" and timerdata[node][STATE]>0:
						timerdata[node][POWER]=1


			
				debug.Info("Look for a change in state")
				if timerdata[node][OLDSTATE] != timerdata[node][STATE]:
					error = zwave.set_node(timerdata[node][ZWAVEPORT], timerdata[node][ZWAVETYPE], timerdata[node][STATE])
					#zerror(error)
					if error == 0:
						debug.Info("    Heating Set OK")
					else:
						debug.Info("    Heating NOT OK")
						timerdata[node][STATE] = timerdata[node][OLDSTATE]

		

		if cmd=="STATUS":
			
			debug.Info("Status Command")
		
#		# Send a SMS if needed
#		# ====================
#		if needsms==1:
#			msg = status_string_sms()
#			error=phone.send_sms_message(sender, msg)
#			#perror(error)
		
		ok=True

	except Exception, e:
		debug.Info("EXCEPTION: Problem in process_commands. ["+str(e)+"]")
		ok=False

	debug.Info("--- process_commands ---")
	
	return ok
	



###############################################################################
def process_zwave_timers():
###############################################################################
#
#
#
###############################################################################

	global zwave
#	global phone
	global sock
	global winstuff
	global settings
	global timerdata


	# =============================
	# Z-Wave Responding
	# =============================
	if zwave.isActive()==True and zwave.isResponding()==True:


		# Process every ZWAVE Device in the Database
		# ==========================================
		for device in xrange(NUMBEROFZWAVEDEVICES):
	
			# Check if timer changes on/off status
			# ====================================
			if timerdata[device][TIMER]==1 and timerdata[device][BOOST]==0:


##				print "Checking " + timerdata[device][NAME]

				timerdata[device][OLDSTATE] = timerdata[device][STATE]

				dayofweek = d.weekday()		# Monday is 0 and Sunday is 6
				hourofday = t.hour
				minuteofday = t.minute

				#debug
				#minuteofday+=6

				index=hourofday*2
				if minuteofday>=30 and minuteofday<60:
					index=index+1

				if timerdata[device][dayofweek][index]==1:
					if timerdata[device][ZWAVETYPE]=="LIGHT":
						timerdata[device][STATE]=99	
					else:
						timerdata[device][STATE]=1
				else:
					timerdata[device][STATE]=0

				# Look for a change in on/off status
				if timerdata[device][OLDSTATE] != timerdata[device][STATE]:
					error = zwave.set_node(timerdata[device][ZWAVEPORT], timerdata[device][ZWAVETYPE], timerdata[device][STATE])
					if error != 0:
						debug.Info("Could not read heating status")
						timerdata[device][STATE] = timerdata[device][OLDSTATE]


	
			# Check if Boost needs to stop - Check boost after timer
			# ============================
			if timerdata[device][BOOST]==1:
				timerdata[device][BOOSTELAPSEDTIME] = time.time() - timerdata[device][BOOSTSTARTTIME]
				if timerdata[device][BOOSTELAPSEDTIME] > timerdata[device][BOOSTLENGTH]:

					process_commands("BOOST-"+timerdata[device][ZWAVETYPE]+"-"+str(device),0)	# Implied that Boost is ON so toggle it



				
###############################################################################
def process_any_zwave_commands():
###############################################################################
# Look to see if any ZWave device sent a command
#
#
###############################################################################

	global zwave
#	global phone
	global sock
	global winstuff
	global settings
	global timerdata


	if zwave.isActive()==True and zwave.isResponding()==True:
	
		# Check for a Z-Wave command
		(zwaveid,error) = zwave.check_for_zwave_command()
				
		if zwaveid!=0 and error==0:
			debug.Info("Button ["+str(zwaveid)+"] pressed")

			# Loop thru the Zwave devices to see which node this was
			nodename=""
			nodetype=""
			device=0
			for x in xrange(NUMBEROFZWAVEDEVICES):

				if zwaveid == ord(timerdata[x][ZWAVEPORT]):
					nodename = timerdata[x][NAME]
					nodetype = timerdata[x][ZWAVETYPE]
					device=x

			print "--------------------------------------"
			print "Name is     ["+str(nodename)+"]"
			print "Type is     ["+str(nodetype)+"]"
			print "Zwave ID is ["+str(zwaveid)+"]"
			print "Device is   ["+str(device)+"]"
			print "--------------------------------------"

		
			# If the heating device sent the command, it will be treated as a BOOST command
			# =============================================================================
			if nodetype == "HEATING":

				debug.Info("Mimic a Boost ON")
				process_commands('BOOST-HEATING-'+str(device),0)

			# Signal that light switch was pressed
			# ====================================
			if nodetype == "LIGHT":
				process_commands('DIMMERSWITCH-LIGHT-'+str(device),0)


###############################################################################
#def process_any_sms_commands():
###############################################################################
# This checks the incoming SMS and calls process_commands
#
#
###############################################################################
#	
#	global zwave
#	global phone
#	global sock
#	global winstuff
#	global settings
#	global timerdata
#
#	debug=Debug()	
#	debug.Info1("+++ process_any_sms_commands +++")
#	
#	if phone.isActive()==True and phone.isResponding()==True:	
#
#		# Check for SMS
#		(number, text, error) = phone.get_command_sms()
#		
#		if error==0:
#			if number:
#				try:
#					if (number == sender) or (number == sender1):
#						debug.Info("    Processing SMS message ["+str(text)+"] from ["+str(number)+"]")
#						text = text.upper()
#						if text == "P":
#							debug.Info("Processing a POWER Command")
#							process_commands('POWER-HEATING-0',1)
#						
#						elif text == "B":
#							debug.Info("Processing a BOOST Command")
#							process_commands('BOOST-HEATING-0',1)
#				
#						elif text == "T":
#							debug.Info("Processing a TIMER Command")
#							process_commands('TIMER-HEATING-0',1)
#						
#						elif text == "S":
#							debug.Info("Processing a STATUS Command")
#							process_commands('STATUS-ALL-0',1)
#						else:
#							debug.Info("ERROR: INVALID Command ")
#							x="An invalid SMS command ["+str(text)+"] was received from ["+str(number)+"]"
#							sock.send_email(x)
#							#send_sms_message(sender, x)
#					else:
#						debug.Error("SMS received from unauthorised number ["+str(number)+"]")
#						
#				except Exception, e:
#					debug.Exception("Problem in [process_any_sms_commands]. ["+str(e)+"]")
#	
#	debug.Info1("--- process_any_sms_commands ---")
#				
		
		
		
	
		
		
###############################################################################
#def send_daily_satus():
###############################################################################
# Send the daily status 
#
#
###############################################################################
#
#	global phone
#	global sock
#	global dailystatussent
#	global t
#	
#	
#	debug=Debug()
#	
#	debug.Info1("+++ send_daily_satus +++")
#		
#	#if (t.hour==17) and (t.minute==26):
#	if (t.hour==10) and (t.minute==45):
#		if dailystatussent==False:
#			debug.Info("Send Daily Status")
#
#			msg=status_string("ALL", "email")
#			sock.send_email(msg)
#
#			if phone.isActive() and phone.isResponding():
#				msg=status_string_sms()
#				error=phone.send_sms_message(sender, "DAILY STATUS:"+msg)
#	
#			dailystatussent=True
#	else:
#		dailystatussent=False
#
#	debug.Info1("--- send_daily_satus ---")
	


###############################################################################
#def send_any_alarms():
###############################################################################
# Send an Email and SMS for any alarm conditions
#
#
###############################################################################
#
#	global batteryAlarmIntervalStart
#	global batteryAlarmIntervalEnd
#	global alarmmesagesent
#	
#	debug=Debug()
#	debug.Info1("+++ send_any_alarms +++")
#		
#	if batteryAlarm==1:
#		if alarmmesagesent==False:
#
#			batteryAlarmIntervalStart=time.time()
#
#			debug.Info("=======================================================")
#			debug.Info("  ")
#			debug.Info("Send Alarm Message")
#			debug.Info("  ")
#			debug.Info("========================================================")
#
#			msg=status_string("ALL", "email")
#			sock.send_email(msg)
#
#			if phone.isResponding():
#				msg=status_string_sms()
#				error=phone.send_sms_message(sender, "POWER ALERT:"+msg)
#				
#			alarmmesagesent=True
#
#		if alarmmesagesent==True:
#			batteryAlarmIntervalEnd=time.time()
#
#			if batteryAlarmIntervalEnd - batteryAlarmIntervalStart > batteryAlarmInterval:
#				alarmmesagesent=False
#
#
#		
#	debug.Info1("--- send_any_alarms ---")
#		



###############################################################################
def test_harness():
###############################################################################
#
#
###############################################################################

	###########################################################################
	# General
	###########################################################################
	# Class Harness
	# =============
	if 0:
		debug=Debug()
		debug.Info 		("Info - 0")
		debug.Warning	("Warning - 1")
		debug.Error		("Error - 0")
		sys.exit(1)

	# Misc Harness
	# ============
	if 0:
		now = datetime.datetime.now()
		print now.year, now.month, now.day, now.hour, now.minute, now.second
		sys.exit(1)

	# log file backup harness
	# =======================
	if 0:
		debug=Debug()
		debug.BackupLogfile()
		sys.exit(1)
	

	# Conversion Test Harness
	# =======================
	if 0:
		status = "\x1f"
		print status
		print ord(status)
		sys.exit(1)	
	

	# Routine Checks
	# ==============
	if 0:
		
		zwave=Zwave()
		phone=Phone()
		winstuff=Winstuff()
		key=""
		while key != 'Q':
			if msvcrt.kbhit():
				sys.exit(1)			
			
			now = datetime.datetime.now()
			d = now.date()
			t = now.time()
			
			#routine_check_on_zwave()
			#routine_check_on_phone()
			
			#check_to_restart_phone()
			#check_to_restart_zwave()
			check_laptop_power()
		sys.exit(1)	


	# dailystatussent
	# ===============
	if 0:
		now = datetime.datetime.now()
		d = now.date()
		t = now.time()
		
		dailystatussent=False
		send_daily_satus(t)
		print dailystatussent
		sys.exit(1)	
		

	
	###########################################################################
	# Phone
	###########################################################################
	# Init
	# ================
	if 0:
		phone=Phone()
		sys.exit(1)

	
	
	# Send SMS Harness
	# ================
#	if 0:
#		phone=Phone()
#		if phone.isActive():
#			if phone.isResponding():
#				msg="Hello"
#				error=phone.send_sms_message(sender, msg)
#				print "====================="
#				print error
#				print "====================="
#		
#		sys.exit(1)


	# Get SMS Harness
	# ================
#	if 0:
#		phone=Phone()
#		if phone.isActive():
#			if phone.isResponding():
#				(number, message, error)=phone.get_command_sms()
#				print "====================="
#				print number
#				print message
#				print error
#				print "====================="
#		
#		sys.exit(1)


	# Get Phone Info
	# ==============
	if 0:
		phone=Phone()
		if phone.isActive():
			if phone.isResponding():
			
				(imei, imei_error) 		= phone.get_imei()
				(batt, batt_error) 		= phone.get_battery()
				(signal, signal_error) 	= phone.get_signal()
				
				print "====================="
				print imei, imei_error
				print batt, batt_error
				print signal, signal_error
				print "====================="
		
		sys.exit(1)



	
	###########################################################################
	# Zwave
	###########################################################################
	
	if 0:
		zwave=Zwave()
		sys.exit(1)
	
	
	if 0:
		zwave=Zwave()
		if zwave.isActive():
			if zwave.isResponding():
				error = zwave.set_node(timerdata[LIGHT1][ZWAVEPORT], timerdata[LIGHT1][ZWAVETYPE], 0)
				time.sleep(4)
				error = zwave.set_node(timerdata[LIGHT1][ZWAVEPORT], timerdata[LIGHT1][ZWAVETYPE], 20)
				
				print "====================="
				print error
				print "====================="
	
		sys.exit(1)

		
	if 0:
		zwave=Zwave()
		if zwave.isActive():
			if zwave.isResponding():
				(status, error) = zwave.get_node(timerdata[LIGHT1][ZWAVEPORT], timerdata[LIGHT1][ZWAVETYPE])
				
				print "====================="
				print error, status
				print "====================="
	
		sys.exit(1)

	if 0:
		zwave=Zwave()
		if zwave.isActive():
			if zwave.isResponding():
				(node, error) = zwave.check_for_zwave_command()

				print "====================="
				print error, node
				print "====================="

		sys.exit(1)
	

	
	###########################################################################
	# Socket
	###########################################################################
	# Home Network Harness
	# ====================
	if 0:
		sock=SocketControl()
		sock.detectHomeNetwork()
		sys.exit(1)
	
	# Email Test Harness
	# ==================
	if 0:
		sock=SocketControl()
		msg="Hello Dave"
		sock.send_email(msg)
		sys.exit(1)


	# Get IP Address
	# ==================
	if 0:
		sock=SocketControl()
		addr=sock.get_ip_address()
		print "====================="
		print addr
		print "====================="
		sys.exit(1)

	
	

	###########################################################################
	# Windows
	###########################################################################
	# Laptop battery
	# ==============
	if 0:
		winstuff=Winstuff()
		(batteryStatus, estimatedChargeRemaining, text) = winstuff.getLaptopPower()
		print "====================="
		print batteryStatus
		print estimatedChargeRemaining
		print text
		print "====================="
		sys.exit(1)
		
	
	
	
	
	
	
	###########################################################################
	# Status
	###########################################################################
	# General
	# ==============
	if 0:
		zwave=Zwave()
		phone=Phone()
		sock=SocketControl()
		winstuff=Winstuff()
		
		#print status_string_sms()
		print status_string("ALL", "html")
		
		
		
		sys.exit(1)
		
	

		



###############################################################################
#
#							M A I N   F U N C T I O N
#
###############################################################################
if __name__=='__main__':

	debug = Debug()

	debug.Info ("================================================================")
	debug.Info ("Control Program")
	debug.Info ("================================================================")

	
	
	# Test Harness
#	test_harness()




	# Open Devices
	# ===========
	zwave=Zwave()
#	phone=Phone()
	sock=SocketControl()
#	winstuff=Winstuff()


	
#	debug.BackupLogfile()	
	
	
	settings=Settings()
	if settings.is_settings_file():
		timerdata=settings.read_settings()
	else:
		settings.save_settings(timerdata)
		sys.exit()
	
	
	

	###########################################################################
	# 	MAIN LOOP
	###########################################################################
	key = ""
	while key != 'Q':
		if isWin():
			if msvcrt.kbhit():
				key = msvcrt.getch()
				process_keyboard_command(key)
		else:
			if kbhit():
				key = getch()
				process_keyboard_command(key)
		



		
		# Get time globals for Scheduled Tasks
		now = datetime.datetime.now()
		d = now.date()
		t = now.time()
		
		process_any_zwave_commands()
#		process_any_sms_commands()	
		process_any_socket_commands()
	
		process_zwave_timers()
	
#		check_to_restart_phone()
		check_to_restart_zwave()
		
#		check_laptop_power()		
		
#		routine_check_on_phone()
		routine_check_on_zwave()		
		
#		send_daily_satus()
#		
#		send_any_alarms()
		
		
		
##		#debug.Info("Laptop Power ["+str(batteryValue)+"-"+str(batteryCharge)+"-"+str(batteryText)+"] Sent["+str(dailystatussent)+"]"
##		for device in xrange(NUMBEROFZWAVEDEVICES):
##			debug.Info(timerdata[device][NAME]+": Power["+str(timerdata[device][POWER])+"] Timer["+str(timerdata[device][TIMER])+"] Boost["+str(timerdata[device][BOOST])+"] Boost Elaps["+str(timerdata[device][BOOSTELAPSEDTIME])+"] State["+str(timerdata[device][STATE])+"]")
##			
##		#Min["+str(t.minute)+"] Sec["+str(t.second)+"] Phone["+str(phone)+"] Phone Resp["+str(phone_responding)+"] ZWave["+str(zwave)+"]  ZWave Respond["+str(zwave.isResponding())+"]")
		
		# debug
		#if phone == False:
		#	time.sleep(1)
		
	settings.save_settings(timerdata)

