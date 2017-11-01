#!c:\python27\python.exe

import sys
import time

####import serial							# http://pyserial.sourceforge.net/index.html
from messaging.sms import SmsSubmit		# http://minimoesfuerzo.org/2010/04/18/python-messaging-sms-encoderdecoder-masses/
from messaging.sms import SmsDeliver

sys.path.append("./common")
import debug
from debug import *
from winstuff import *



###############################################################################
class Phone ():
###############################################################################

	__porttimeout=1					# Seconds for serial port timeout
	__maxportwait=10				# Seconds to wait for phone to respond
	__baud=115200					# __baud rate
	
	__WINDOWSNAME = "s125mgmt"		# SE K310i - Windows Registary name for Phone Port
	#__WINDOWSNAME = "s0017mgmt"	# SE K880i - Windows Registary name for Phone Port
	
	__hPhone=None					# Handler
	__responding=False				# Flag to indicate phone is responding or not

	
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
	# Sets up the serial port for use with the mobile phone
	#
	# Returns:	True if port setup was successful
	#			False if port setup failed
	###############################################################################
		
		Phone.init_phone(self)


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
			Phone.__responding=True
		else:
			Phone.__responding=False
			
			

	###############################################################################
	def __modem_reset(self):
	###############################################################################
	# Sends an ATZ to the modem
	#
	# Returns	-2
	#			-1
	#			0
	###############################################################################

		debug=Debug()
		
		debug.Info ("+++ modem_reset +++")

		try:
			debug.Info ("    Send AT Command [ATZ]")
			(resp,error)=Phone.__send_at(self, 'ATZ')

			if error==0:
				if resp == "":
					debug.Error ("    Problem in device")
					error=-1

				elif (resp.find("OK") > 0):
					debug.Info ("    Modem reset OK")
					

		except Exception, e:
			debug.Exception("Problem is modem reset. ["+str(e)+"]")
			error=-1

		debug.Info ("--- modem_reset ---")
		Phone.__error(self, error)
		return error




	###############################################################################
	def __send_at(self, cmd):
	###############################################################################
	# Send a command to the phone
	#
	# Returns	Response from phone if successful
	#			Empty string if a problem
	#
	# Returns	-2
	#			-1
	#			0
	###############################################################################

		debug=Debug()
		
		debug.Info1 ("+++ send_at +++")

		response=""
		error=0

		try:
			if Phone.__hPhone:

				try:
					debug.Info1 ("    Write the AT Command ["+str(cmd)+"]") 
					Phone.__hPhone.write(cmd+"\r")
				except:
					debug.Exception("Could not write ["+str(cmd)+"] to Serial Port")
					error=-2

				if error==0:
					debug.Info1 ("    Wait for response...")
					(response,error)=Phone.__wait_for_data(self)

					if error==0:
						debug.Info1 ("    Data read is "+str(response))

						debug.Info1 ("    Looking for OK")
						if (response.find("OK") > 0):
							debug.Info1 ("    Data read OK")
						else:
							debug.Error("An error was returned from the AT Command ["+str(cmd)+"]")
							response=""
							error=-1
			else:
				debug.Error("Port not found")
				error=-2

		except Exception, e:
			debug.Exception ("EXCEPTION: Problem in send_at. ["+str(e)+"]")
			response=""
			error=-1

		debug.Info1 ("--- send_at --- Error["+str(error)+"]")
		Phone.__error(self, error)
		return response, error



	###############################################################################
	def __wait_for_data(self):
	###############################################################################
	# Checks serial port for data and will wait until a timeout expires
	#
	# Returns data read from port, empty string if no data read
	#
	# Returns	-2
	#			-1
	#			0
	################################################################################
	
		debug=Debug()
		debug.Info1 ("+++ wait_for_data +++")
		
		response=""
		error=0
		byteCount=0
		
		try:
			if Phone.__hPhone:
				wait_start=time.time()
				wait=True
				while wait:
						
					try:
						
						if Phone.__hPhone.inWaiting() > 0:
								
							byteCount = Phone.__hPhone.inWaiting()
							response += Phone.__hPhone.read(byteCount)
							
							if (response.endswith("\nOK\r\n")):
								wait=False
						
						wait_stop = time.time()
						if wait_stop - wait_start > Phone.__maxportwait:
							wait=False
						else:
							time.sleep(0.5)
						
					except:
						debug.Exception ("Problem reading port")
						error=-2
						wait=False
			
			else:
				debug.Warning ("ERROR: No serial port")
				error=-2
				
		except Exception, e:
			debug.Exception ("Problem in wait_for_data. ["+str(e)+"]")
			response=""
			error=-1
		
		debug.Info1 ("--- wait_for_data ---")
		Phone.__error(self, error)
		return response, error
	
	
	
	
	###############################################################################
	def __set_storage(self):
	###############################################################################
	# Sets up the SMS storage location
	#
	# Returns	-2
	#			-1
	#			0
	###############################################################################
	
		debug=Debug()
		debug.Info ("+++ set_storage +++")
		
		error=0
		
		try:
			debug.Info ("    Setting SMS Storage to ME")
			(response,error)=Phone.__send_at(self, 'AT+CPMS="ME"')
			#(response,error)=Phone.__send_at(self, 'AT+CPMS="SM"')
			
			if error==0:
				debug.Info ("    Data written OK")
	
				if response != "":
					if (response.find("OK") > 0):
						debug.Info ("    Command Accepted")
						
					else:
						debug.Warning ("    Command NOT Accepted")
						error=-1
			else:
				debug.Error("Command not written")
				error=-2
				
		except Exception, e:
			debug.Exception("Problem in set_storage. ["+str(e)+"]")
			error=-1
				
		debug.Info ("--- set_storage ---")
		Phone.__error(self, error)
		return error
	

	###############################################################################
	def __del__ (self):
	###############################################################################
	#
	#
	#
	###############################################################################

		debug = Debug()		

		debug.Info("++++ Phone Destructor ++++")

		
		if Phone.__hPhone:
			debug.Info("    Closing Phone")
			Phone.__hPhone.close()
		else:
			debug.Info("    Phone Port already closed")
			
		debug.Info("    Done")

		debug.Info("---- Phone Destructor ----")		



	
	
	###############################################################################
	# 
	#							Public Methods
	#
	###############################################################################
	# 
	#
	###############################################################################
	
	
	###############################################################################
	def init_phone(self):
	###############################################################################
	# Sets up the serial port for use with the mobile phone
	#
	# Returns:	True if port setup was successful
	#			False if port setup failed
	###############################################################################
		
		debug=Debug()
		debug.Info ("+++ init_phone +++")

		Phone.__responding=False

		try:
			debug.Info ("    Close any open ports")
			if Phone.__hPhone:
				Phone.__hPhone.close()

			debug.Info ("    Scan Windows Registry for Phone port")
			winstuff=Winstuff()
			port = winstuff.scan(Phone.__WINDOWSNAME)
			
			if port != 0:
				port = port - 1

				debug.Info ("    Opening Phone Port ["+str(port)+"]...")
				#Phone.__hPhone = serial.Serial(port, baudrate=__baud, timeout=__porttimeout,writeTimeout=__porttimeout, interCharTimeout=__porttimeout)
				#Phone.__hPhone = serial.Serial(port, baudrate=__baud)
				Phone.__hPhone = serial.Serial(port, baudrate=Phone.__baud, timeout=None,writeTimeout=None, interCharTimeout=None)
				

				if Phone.__hPhone:
					debug.Info ("    Port opened OK ["+str(Phone.__hPhone)+"]")
					if Phone.__modem_reset(self) == 0:
						if Phone.__set_storage(self) == 0:
							Phone.__responding=True
				else:
					debug.Error ("Problem in opening port")
					Phone.__hPhone=None
			else:
				debug.Error ("ERROR: Port not found")
				Phone.__hPhone=None


		except Exception, e:
			debug.Exception ("Problem in init_phone. ["+str(e)+"]")
			Phone.__hPhone=None

		debug.Info ("--- init_phone ---")
		

	
	
	
	###############################################################################
	def isActive(self):
	###############################################################################
	# 
	#
	# 
	#
	#
	###############################################################################
		
		if Phone.__hPhone:
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
		
		return Phone.__responding



	

	###############################################################################
	def send_sms_message(self, number, text):
	###############################################################################
	# Send an SMS
	#
	# Returns 	-2
	#			-1
	#			0
	###############################################################################

		debug=Debug()
		debug.Info ("+++ send_sms_message +++")
		debug.Info ("    Message ["+str(text)+"] ")
		debug.Info ("    Number  ["+str(number)+"]")

		error=0

		try:

			debug.Info ("    Encode the SMS - cater for multiple fragements")

			sms = SmsSubmit(number, text)
			sms.ref = 0x0
			sms.rand_id = 136

			ret = sms.to_pdu()

			for i, pdu in enumerate(ret):
				debug.Info ("    Sending fragement " + str(i))
				debug.Info ("    PDU is " + str(pdu.pdu))
				debug.Info ("    Length is " + str(pdu.length))

				cmd='AT+CMGS=%d\n\r' % pdu.length
				debug.Info ("    Write the PDU length ["+str(cmd)+"]") 

				try:
					Phone.__hPhone.write(cmd)
				except:
					debug.Exception("Could not write to serial port")
					error=-2

				if error==0:
					debug.Info ("    Wait for prompt response...")
					(response,error)=Phone.__wait_for_data(self)
					debug.Info ("    Prompt response is\n\n "+str(response))

					if error==0:
						debug.Info ("    Now write one byte at a time")

						# As we cannot write any more than 255 bytes at a time, do a loop here
						for x in pdu.pdu:
							#debug.Info ("    Writing ["+str(x)+"]")
							try:
								Phone.__hPhone.write(str(x))
							except:
								debug.Exception("Could not write byte to serial port")
								error=-2


						if error==0:
							debug.Info("    Now write the Ctrl+z escape")
							try:
								Phone.__hPhone.write('\x1a')
							except:
								debug.Exception("Could not Ctrl-Z byte to serial port")
								error=-2

							if error==0:
								debug.Info ("    Wait for PDU send response...")
								(response,error)=Phone.__wait_for_data(self)

								if error==0:
									debug.Info ("    Data read is \n"+str(response))
									debug.Info ("    Looking for OK")
									if (response.find("OK") > 0):
										debug.Info ("    OK found")
										error=0

				else:
					debug.Error("An error was returned from the AT Command")


		except Exception, e:
			debug.Exception("Problem in send_sms_message. ["+str(e)+"]")
			error=-1

		
		
		if error==-1:
			Phone.__isResponding=False
		else:
			Phone.__isResponding=True
	

		debug.Info ("--- send_sms_message ---")
		Phone.__error(self, error)
		return error



	


	###############################################################################
	def get_command_sms (self):
	###############################################################################
	# Checks for a new SMS message
	#
	# Retruns 	number of any new SMS
	#			message of any new SMS command
	#
	# Returns	-2
	#			-1
	#			0
	###############################################################################

		debug=Debug()
		debug.Info1 ("+++ get_command_sms +++")

		number = ""
		message = ""
		error=0

		try:
					
			#(response,error)=Phone.__send_at(self, 'AT')
			(response,error)=Phone.__send_at(self, 'AT+CMGL=4')
			#(response,error)=Phone.__send_at(self, 'AT+CMGR=1')

			if error==0:
				if response == "":
					debug.Info ("    Problem in device")

				elif (response.find("+CMGL:") > 0):

					debug.Info ("    Parse the response for the PDU")
					a = response.split("\n")
					pdu = a[2].replace("\r", "")

					debug.Info ("    Parse the response for message index")
					b = a[1].replace("+CMGL: " , "")
					b = b.split(',')
					index = b[0]

					debug.Info ("    Extract the info")
					sms = SmsDeliver(str(pdu))
					number =  sms.number
					message =  sms.text

					debug.Info ("    Number ["+str(number)+"] - Index ["+str(index)+"] - Message ["+str(message)+"]")

					debug.Info ("    Delete message")
					(response,error) = Phone.__send_at(self, "AT+CMGD="+index)
					if error==0:
						if (response.find("OK") > 0):
							debug.Info ("    Message deleted OK")
						else:
							debug.Error("Message not deleted")

				else:
					debug.Info1 ("    No new messages available")
					number=""
					response=""

			else:
				debug.Error("Problem in reading SMS")

		except Exception, e:
			debug.Exception("Problem in get_command_sms. ["+str(e)+"]")
			number=""
			message=""
			error=-1

		debug.Info1 ("--- get_command_sms --- Number["+str(number)+"] Message["+str(message)+"] Error["+str(error)+"]")
		Phone.__error(self, error)
		return number, message, error



	###############################################################################
	def get_imei(self):
	###############################################################################
	# 
	#
	###############################################################################

		debug=Debug()
		debug.Info ("+++ get_imei +++")

		imei=""
		error=0

		try:
			debug.Info ("    Send AT Command")
			(imei,error)=Phone.__send_at(self, 'AT+CGSN')

			if error==0:
				if imei == "":
					debug.Info ("    Problem in device")
					error=-1

				elif (imei.find("OK") > 0):
					# Parse the IMEI from the response
					a = imei.split("\n")
					imei = a[1].replace("\r", "")

		except Exception, e:
			debug.Exception("Problem is getting IMEI. ["+str(e)+"]")
			imei=""
			error=-1

		debug.Info ("--- get_imei ---")
		Phone.__error(self, error)
		return imei, error
		


	###############################################################################
	def get_signal(self):
	###############################################################################
	# 
	#
	###############################################################################

		debug=Debug()
		debug.Info ("+++ get_signal +++")

		global __hPhone

		signal=""
		error=0

		try:
			debug.Info ("    Send AT Command")
			(signal,error)=Phone.__send_at(self, 'AT+CSQ')

			if error==0:
				if signal  == "":
					debug.Info ("    Problem in device")
					error=-1

				elif (signal.find("OK") > 0):

					# Parse the Signal RSSI from the response
					a = signal.split("\r")
					signal = a[1].replace("\n", "")
					signal = signal.replace("+CSQ: ", "")
					a = signal.split(',')
					signal = a[0]

		except Exception, e:
			debug.Exception("Problem is getting Signal. ["+str(e)+"]")
			signal=""
			error=-1

		debug.Info ("--- get_signal ---")
		Phone.__error(self, error)
		return signal, error



	###############################################################################
	def get_battery(self):
	###############################################################################
	# 
	#
	###############################################################################

		debug=Debug()
		debug.Info ("+++ get_battery +++")

		global __hPhone

		battery=""
		error=0

		try:
			debug.Info ("    Send AT Command")
			(battery,error)=Phone.__send_at(self, 'AT+CBC')

			if error==0:
				if battery == "":
					debug.Info ("    Problem in device")
					error=-1

				elif (battery.find("OK") > 0):
					# Parse the battery from the response
					a = battery.split("\r")
					battery = a[2].replace("\n", "")
					battery = battery.replace("+CBC: ", "")
					a = battery.split(',')
					battery = a[1]
					battery = battery.replace(" ", "")

		except Exception, e:
			debug.Exception("Problem is getting Battery. ["+str(e)+"]")
			battery=""
			error=-1

		debug.Info ("--- get_battery ---")
		Phone.__error(self, error)
		return battery, error





