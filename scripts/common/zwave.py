# !c:\python25\python.exe

import sys
import time
import serial						# http://pyserial.sourceforge.net/index.html - yum install pyserial
from binascii import hexlify

sys.path.append("./common")
from debug import *
from common import *

if isWin():
	from winstuff import *


###############################################################################
class Zwave ():
###############################################################################


	__porttimeout=1						# Seconds for serial port timeout
	__baud=115200						# __baud
	__portwait=0.5						# Seconds to wait between ZWave commands
	__WINDOWSNAME = "ProlificSerial"	# Windows Registary name for Zwave Port
	__hZwave=None						# Handler
	__responding=False					# Flag to indicate phone is responding or not



	###############################################################################
	# 
	#							Private Methods
	#
	###############################################################################
	# 
	#
	###############################################################################
		
	


	
	###############################################################################
	def __init__(self):
	###############################################################################
	# Setup the serial port for use with Zwave
	#
	# Returns:	True if port setup was successful
	#			False if port setup failed
	###############################################################################
	
		Zwave.init_zwave(self)
	
	
	###############################################################################
	def __error(self, x):
	###############################################################################
	# Sets any error flags
	#
	# 
	#
	#			
	###############################################################################

		if x==0:
			Zwave.__responding=True
		else:
			Zwave.__responding=False





	
	###############################################################################
	def __wait_for_ok_response (self, wait_for_string):
	###############################################################################
	# Reads the Z-Wave serial port
	#
	# Can wait for a certain return sequence
	#
	# Returns:	Actual sequence if if not searching of a sequence
	#			Empty string if no response at all
	#			0 if sequence found
	#			1 if sequence not found
	#
	# Returns	-1 if Z-Wave not responding
	#			-2 if Z-Wave not availale
	#			0 if no Z-Wave error
	###############################################################################
		
		debug=Debug()
		debug.Info1 ("+++ wait_for_ok_response +++")
		
		response=""
		error=0
		
		try:
			if Zwave.__hZwave:
				time.sleep(0.25)
	
				try:
					while Zwave.__hZwave.inWaiting() > 0:
						response += Zwave.__hZwave.read(1)
				except:
					debug.Exception ("Problem in reading ZWave port")
					error=-2
					
				if response and error==0:
					debug.Info ("    Response is ["+hexlify(response)+"]")
					if wait_for_string:
						debug.Info ("    Waiting for ["+hexlify(wait_for_string)+"]")
						if response == wait_for_string:
							response=0		
							debug.Info ("    OK - Response found")
						else:
							response=1		
							error=-1
							debug.Error ("    Response NOT found")
				else:
					debug.Info1 ("    No data")
			else:
				debug.Error ("No Z-Wave Port Open!")
				error=-2
		except Exception, e:
			debug.Exception ("Problem in wait_for_ok_response. ["+str(e)+"]")
			error=-2
				
		debug.Info1 ("--- wait_for_ok_response ---")
		Zwave.__error(self, error)
		return response, error
	
	


	
	###############################################################################
	def __send_command(self, cmd):
	###############################################################################
	# Sends a sequence to the Z-Wave port
	#
	# Returns	True if command was successful
	#			False if command failed to send
	###############################################################################
	
		debug=Debug()
		debug.Info ("+++ send_command +++")
		debug.Info ("    Sending command ["+hexlify(cmd)+"]")
				
		ok=False
	
		try:
			if Zwave.__hZwave:
				Zwave.__hZwave.write(cmd)
				ok=True
			else:
				debug.Error ("No Z-Wave Port Open")
				
		except Exception, e:
			debug.Exception("Problem sending command ["+hexlify(cmd)+"]. ["+str(e)+"]")
			ok=False
	
		debug.Info ("--- send_command ---")
		return ok
		


	
	###############################################################################        
	def __send_ack (self):
	###############################################################################
	# Sends an ACK to the Z-Wave controller
	#
	# Returns	0 if OK
	#			1 if not OK
	###############################################################################
	
		debug=Debug()
		debug.Info ("--- send_ack ---")	
		
		cmd = "\x06"
		error=1
		
		try:
			if Zwave.__hZwave:
				debug.Info ("    Sending ACK ["+hexlify(cmd)+"]")
				Zwave.__hZwave.write(cmd)
				error=0
			else:
				debug.Error ("No ZWave Port Open")
				
		except Exception, e:
			debug.Exception ("Problem in sending ACK. ["+str(e)+"]")
							
		debug.Info ("--- send_ack ---")	
		Zwave.__error(self, error)
		return error
	
	
	

	###############################################################################
	def __addChecksum(self, message):
	###############################################################################
	# Add the checksum to the end of the command
	#
	###############################################################################

		lrc = 0xFF
		for b in message:
			lrc ^= ord(b)
		message += chr(lrc)
		return message
	


	###############################################################################
	def __del__ (self):
	###############################################################################
	#
	#
	#
	###############################################################################

		debug = Debug()		
		debug.Info("++++ Zwave Destructor ++++")

		
		if Zwave.__hZwave:
			debug.Info("    Closing Zwave")
			Zwave.__hZwave.close()
		else:
			debug.Info("    Zwave Port already closed")
			
		debug.Info("    Done")

		debug.Info("---- Zwave Destructor ----")		

	
	
	
	


	###############################################################################
	# 
	#							Public Methods
	#
	###############################################################################
	# 
	#
	###############################################################################


	###############################################################################
	def init_zwave(self):
	###############################################################################
	# Setup the serial port for use with Zwave
	#
	# Returns:	True if port setup was successful
	#			False if port setup failed
	###############################################################################
	
		debug=Debug()
		debug.Info ("+++ init_zwave +++")
		
		Zwave.__responding=False
		
		try:
		
			debug.Info ("    Close any open ports")
			if Zwave.__hZwave:
				Zwave.__hZwave.close()
		
			debug.Info ("    Scan Windows Registry for Z-Wave port")
			
			if isWin():
				winstuff=Winstuff()
				usbport = winstuff.scan(Zwave.__WINDOWSNAME)
			else:
				usbport = "/dev/ttyUSB1"
			
			
			if usbport != 0:
	
				if isWin():
					usbport = usbport - 1
					
				debug.Info ("    Opening COM Port ["+str(usbport)+"] for Z-Wave")
				#Zwave.__hZwave = serial.Serial(usbport, baudrate=Zwave.__baud, timeout=Zwave.__porttimeout) 
				#Zwave.__hZwave = serial.Serial(int("4"), baudrate=Zwave.__baud, timeout=Zwave.__porttimeout) 
				ser = serial.Serial("COM4", 9600)
	
				if Zwave.__hZwave:
					debug.Info ("    Port opened OK ["+str(Zwave.__hZwave)+"]")
	
					Zwave.__hZwave.flushInput()
					Zwave.__hZwave.flushOutput()
	
					# Clear out any previous responses
					Zwave.__wait_for_ok_response(self, None)
	
					debug.Info ("Do some setup - Mimic the SampleApp")
					Zwave.__send_command(self, "\x01\x03\x00\x15\xE9")
					Zwave.__wait_for_ok_response(self, "\x06\x01\x10\x01\x15\x5A\x2D\x57\x61\x76\x65\x20\x32\x2E\x36\x34\x00\x01\x96")
					Zwave.__send_ack(self)
					Zwave.__send_command(self, "\x01\x0A\x00\x03\x02\x02\x01\x03\x20\x86\x88\xDA")
					Zwave.__wait_for_ok_response(self, "\x06")
	
	
					#Zwave.__send_command(self, "\x01\x03\x00\x20\xDC")
					#Zwave.__wait_for_ok_response(self, "\x06\x01\x08\x01\x20\x00\xCE\x03\x40\x01\x5A")
					#Zwave.__send_ack(self)
	
					debug.Info ("    =================")
					debug.Info ("    Network Discovery")
					Zwave.__send_command(self, "\x01\x03\x00\x02\xFE")
					(response,error) = Zwave.__wait_for_ok_response(self, None)
					Zwave.__send_ack(self)
					length = ord(response[7]) - 1
					index = 1
					for i in range(0, length):
						buffer_index = response[8+i]
						num = 1
						j = 0
						while j <= 7:
							if (ord(buffer_index) & num > 0):
								debug.Info ("    Node ["+str(index)+"] exists")
							index = index+1
							if j < 7:
								num = num * 2
							j = j+1
					debug.Info ("    =================")
					#Zwave.__wait_for_ok_response(self, "\x06\x01\x25\x01\x02\x05\x00\x1D\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01\xD2")
					#Zwave.__send_ack(self)
	
	
					#Zwave.__send_command(self, "\x01\x04\x00\x41\x01\xBB")
					#Zwave.__wait_for_ok_response(self, "\x06\x01\x09\x01\x41\x12\x96\x00\x01\x02\x01\x30")
					#Zwave.__send_ack(self)
	
					#Zwave.__send_command(self, "\x01\x04\x00\x41\x05\xBF")
					#Zwave.__wait_for_ok_response(self, "\x06\x01\x09\x01\x41\xD2\x94\x00\x03\x10\x01\xE2")
					#Zwave.__send_ack(self)
	
					debug.Info ("    Done")
					Zwave.__responding=True
	
				else:
					debug.Error ("Problem in opening Z-Wave port")
					Zwave.__hZwave=None
			else:
				debug.Error ("Port not found for Z-Wave")
				Zwave.__hZwave=None		
			
		except Exception, e:
			debug.Exception ("Problem in init_zwave. ["+str(e)+"]")
				
		debug.Info ("--- init_zwave ---")
		
	
	

	###############################################################################
	def isActive(self):
	###############################################################################
	# 
	#
	# 
	#
	#
	###############################################################################
		
		if Zwave.__hZwave:
			return True
		else:
			return False
		
		
	###############################################################################
	def isResponding(self):
	###############################################################################
	# 
	#
	# 
	#
	#
	###############################################################################
		
		return Zwave.__responding



	###############################################################################
	def get_node(self, node, function):
	###############################################################################
	# Reads the status of a node
	#
	# Returns	0 if set
	#			1 if not set
	# Returns	-1 if Z-Wave not responding
	#			-2 if Z-Wave not availale
	###############################################################################
		
		debug=Debug()
		debug.Info ("+++ get_node +++")
		debug.Info ("    Getting Node ["+str(ord(node))+"]")
		
		error=-2
		response=None
		status=0
		
		try:
			# Snoops of Sample App
			# ====================
			#
			# Get when OFF
			#01#09#00#13#05#02#25#02#05#03#C3
			#06#01#04#01#13#01#E8
			#06
			#01#05#00#13#03#00#EA
			#06
			#01#09#00#04#00#05#03#25#03#00#D2
			#06
	
			# Get when ON
			#01#09#00#13#05#02#25#02#05#03#C3
			#06#01#04#01#13#01#E8
			#06
			#01#05#00#13#03#00#EA
			#06
			#01#09#00#04#00#05#03#25#03#FF#2D
			#06
			
			
			# Tweak for Switch and Dimmer
			if (function=="SOCKET") or (function=="HEATING"):
				tweak='\x25'
			
				#if status==1:
				#	status = '\xff'
				#elif status==0:
				#	status = '\x00'
						
			elif (function=="LIGHT"):
				tweak='\x26'
				#status=chr(status)
			else:
				# Default
				tweak='\x00'
				#status = '\x00'
					
		
			if Zwave.__hZwave:	
				debug.Info ("    Create command")	
				cmd="\x09\x00\x13"+node+"\x02"+tweak+"\x02\x05\x03"
	
				debug.Info ("    Add checksum")
				cmd = Zwave.__addChecksum(self, cmd)
				cmd = "\x01"+cmd
	
				try:
					debug.Info ("    Sending command ["+hexlify(cmd)+"]")
					Zwave.__hZwave.write(cmd)
					error=0
				except Exception, e:
					debug.Exception ("Problem in sending command ["+hexlify(cmd)+"]. ["+str(e)+"]")
					error=-2
	
				if error == 0:
					debug.Info ("    Wait #1")
					(response,error)=Zwave.__wait_for_ok_response(self, None)
					debug.Info ("    Received    ["+hexlify(response)+"]")
	
					debug.Info ("    Send ACK #1")
					error=Zwave.__send_ack(self)
	
					debug.Info ("    Wait #2")
					(response,error)=Zwave.__wait_for_ok_response(self, None)
					debug.Info ("    Received    ["+hexlify(response)+"]")
	
					debug.Info ("    Send ACK #2")
					error=Zwave.__send_ack(self)
	
					debug.Info ("    Wait #3")
					(response,error)=Zwave.__wait_for_ok_response(self, None)		# This is where the status lives
					debug.Info ("    Response is ["+hexlify(response)+"]")
	
					debug.Info ("    Send ACK #3")
					error=Zwave.__send_ack(self)
	
				if response:
					status = response[9]
					debug.Info ("    HEX Status received ["+hexlify(status)+"]")
					
					debug.Info ("    Convert it")
					if (function=="SOCKET") or (function=="HEATING"):
						if status == "\x00":
							status=0
						else:
							status=1
					else:
						status=ord(status)
						
					debug.Info ("    Status is ["+str(status)+"]")
				else:
					error=-1
					
			else:
				debug.Info ("ERROR: No Z-Wave Port Open")
				error = -2
				
		except Exception, e:
			debug.Exception ("EXCEPTION: Problem in get_node. ["+str(e)+"]")
			error=-1
		
		debug.Info ("    Error  ["+str(error)+"]")
		debug.Info ("    Status ["+str(status)+"]")
		
		debug.Info ("--- get_node ---  ")
		Zwave.__error(self, error)
		return status, error




	###############################################################################
	def set_node(self, node, function, status):
	###############################################################################
	# Sets the node of a Z-Wave device to a certain value
	#
	# Returns	-1 if Z-Wave not responding
	#			-2 if Z-Wave not availale
	#			0 if no Z-Wave error
	###############################################################################

		debug=Debug()
		debug.Info ("+++ set_node +++")
		debug.Info ("    Setting Node ["+str(ord(node))+"] of function ["+function+"] to ["+str(status)+"]")

		error=-2

		try:
			# Switch OFF Capture
			#01#0A#00#13#05#03#25#01#00#05#03#C2
			#06#01#04#01#13#01#E8
			#06
			#01#05#00#13#03#00#EA
			#06

			# Switch ON Capture
			#01#0A#00#13#05#03#25#01#FF#05#03#3D
			#06#01#04#01#13#01#E8
			#06
			#01#05#00#13#03#00#EA
			#06

			# Dimmer - set 30% (0x1e) on ID 02
			# 01 0A 00 13 02 03 26 01 1E 05 03 D8
			# 06 01 04 01 13 01 E8               
			# 06                                 
			# 01 05 00 13 03 00 EA               
			# 06                                 



			if Zwave.__hZwave:
				debug.Info ("    Set status in command")

				# Tweak for Switch and Dimmer
				if (function=="SOCKET") or (function=="HEATING"):
					tweak='\x25'

					if status==1:
						status = '\xff'
					elif status==0:
						status = '\x00'

				elif (function=="LIGHT"):
					tweak='\x26'
					status=chr(status)
				else:
					# Default
					tweak='\x00'
					status = '\x00'



				debug.Info ("    Create the command")	
				cmd="\x0a\x00\x13"+node+"\x03"+tweak+"\x01"+status+"\x05\x03"

				debug.Info ("    Add checksum")
				cmd = Zwave.__addChecksum(self, cmd)
				cmd = "\x01"+cmd

				try:
					debug.Info ("    Sending command ["+hexlify(cmd)+"]")
					Zwave.__hZwave.write(cmd)
					error=0
				except Exception, e:
					debug.Info ("EXCEPTION: Problem in sending command ["+str(hexlify(cmd))+"]. ["+str(e)+"]")
					error=-2


				if error==0:	
					debug.Info ("    Waiting #1")
					(response,error)=Zwave.__wait_for_ok_response(self, "\x06\x01\x04\x01\x13\x01\xE8")

				if error==0:	
					debug.Info ("    Send ACK #1")
					error=Zwave.__send_ack(self)

				if error==0:	
					debug.Info ("    Waiting #2")
					(response,error)=Zwave.__wait_for_ok_response(self, "\x01\x05\x00\x13\x03\x00\xEA")		

				if error==0:	
					debug.Info ("    Send ACK #2")
					error=Zwave.__send_ack(self)

			else:
				debug.Error("No Z-Wave Port Open")
				error=-2

		except Exception, e:
			debug.Exception("Problem in set_node. ["+str(e)+"]")
			error=-1

		debug.Info ("--- set_node ---")
		Zwave.__error(self, error)
		return error




	###############################################################################
	def check_for_zwave_command(self):
	###############################################################################
	# Checks for a Z-Wave input from the controller and returns the node ID that
	# sent the command
	#
	# Returns	Integer node value of the module that sent the command
	#			0 if no command
	#
	# Returns	-1 if Z-Wave not responding
	#			-2 if Z-Wave not availale
	#			0 if no Z-Wave error
	###############################################################################

		debug=Debug()
		debug.Info1 ("+++ check_for_zwave_command +++")

		### Button pressed on switch #5
		# OFF
		#01#0F#00#49#84#05#09#03#10#01#25#27#72#86#75#73#D3
		#06#01#05#00#4A#05#00#B5
		#06
		# ON
		#01#0F#00#49#84#05#09#03#10#01#25#27#72#86#75#73#D3
		#06#01#05#00#4A#05#00#B5
		#06

		# Dimmer button pressed on switch #2
		# 01 14 00 49 84 02 0E 04 11 01 26 27 85 73 70 86 72 EF 20 26 50 F4                              
		# 06 
		# 01 05 00 4A 05 00 B5                        
		# 06  


		node = 0
		error=0

		try:
			if Zwave.__hZwave:
				(response,error) = Zwave.__wait_for_ok_response(self, None)

				if response and error==0:
				#													Socket                    Dimmer   
					if (response[0] == "\x01") and ( (response[1] == "\x0f") or (response[1] == "\x14") ):

						debug.Info1 ("    Command found ["+hexlify(response)+"] ")

						node = response[5]

						debug.Info1 ("    Sending ACK")
						error=Zwave.__send_ack(self)

						if error == 0:
							cmd="\x01"+node+"\x00\x4A\x05\x00"
							cmd = Zwave.__addChecksum(self, cmd)
							cmd = "\x01"+cmd

							if Zwave.__send_command(self, cmd):
								node=ord(node)
								debug.Info ("Button pressed on node ["+str(node)+"]")
							else:
								debug.Info ("Problem in sending command")
						else:
							debug.Info ("Problem in sending ACK")
				else:
					debug.Info1 ("    No command data")
			else:
				debug.Error ("ERROR: No Z-Wave Port Open")
				error=-2

		except Exception, e:
			debug.Exception("Problem in check_for_zwave_command. ["+str(e)+"]")
			error=-1
			node=""

		debug.Info1 ("--- check_for_zwave_command ---")
		Zwave.__error(self, error)
		return node, error













