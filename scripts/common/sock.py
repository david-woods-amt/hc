#!c:\python25\python.exe

import socket
import sys
import select

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib import urlopen


sys.path.append("./common")
from debug import *



###############################################################################
class SocketControl ():
###############################################################################

	__hSocket = None			# Handler
	__HOST    = ''              # Symbolic name meaning the local host
	__PORT    = 50000			# Arbitrary non-privileged port




	###############################################################################
	# 
	#							Private Methods
	#
	###############################################################################
	# 
	#
	###############################################################################
		



	
	###############################################################################
	def __init__ (self):
	###############################################################################
	#
	#
	#
	###############################################################################
	
		SocketControl.init_sock(self)
	
	
	
	###############################################################################
	def __del__ (self):
	###############################################################################
	#
	#
	#
	###############################################################################
	
		debug = Debug()		
			
		
		debug.Info("++++ Socket Destructor ++++")

		debug.Info("    Closing Socket")
		SocketControl.__hSocket.close()
		debug.Info("    Done")

		debug.Info("---- Socket Destructor ----")		
		
	
	




	
	###############################################################################
	# 
	#							Public Methods
	#
	###############################################################################
	# 
	#
	###############################################################################
	

	###############################################################################
	def init_sock (self):
	###############################################################################
	#
	#
	#
	###############################################################################
	
		debug = Debug()		
				
		debug.Info("+++ init_sock +++")
		
		# Set up a Socket to wait and read data
		try:
			SocketControl.__hSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			SocketControl.__hSocket.bind((SocketControl.__HOST, SocketControl.__PORT))
			SocketControl.__hSocket.listen(0)
			debug.Info ("    listening on port ["+str(SocketControl.__PORT)+"]")
		
		except Exception, e:
			debug.Exception ("Failed to set up socket. ["+str(e)+"]")
			SocketControl.__hSocket=None
		
		if socket == None:
			debug.Warning ("***********************************************")
			debug.Warning ("***         Socket could not be setup       ***")
			debug.Warning ("***            Exit from program            ***")
			debug.Warning ("***********************************************")
			
			sys.exit(1)
			
		debug.Info ("--- init_sock ---")
	
	

	
	
	###############################################################################
	def readsocket(self):
	###############################################################################
	#
	#
	#
	###############################################################################
	
		debug = Debug()		
		debug.Info1("+++ readsocket Socket +++")
	
		data=""
		channel=""
		info=""
		
		try:
			if SocketControl.__hSocket:
				is_readable = [SocketControl.__hSocket]
				is_writable = []
				is_error = []
				r, w, e = select.select(is_readable, is_writable, is_error, 0)
				if r:
					channel, info = SocketControl.__hSocket.accept()
	
					debug.Info1("    Socket connection from ["+str(info)+"]")
					data = channel.recv(1000)
					debug.Info1("    Data is ["+str(data)+"]")
					
		except Exception, e:
			debug.Exception ("Problem in reading from socket. ["+str(e)+"]")	
				
		
		debug.Info1("--- readsocket Socket ---")
		return channel, data
		
		
		



	###############################################################################
	def detectHomeNetwork(self):
	###############################################################################
	# Work out if at Home or in the Office and sets global
	# 
	# Needed to determine what email server to use
	#
	###############################################################################

		debug=Debug()

		debug.Info ("+++ detectHomeNetwork +++")

		try:
		
			(hostname, aliaslist, ipaddrlist) = socket.gethostbyname_ex('')

			debug.Info ("    hostname   is ["+str(hostname)+"]")
			debug.Info ("    aliaslist  is ["+str(aliaslist)+"]")
			debug.Info ("    ipaddrlist is ["+str(ipaddrlist)+"]")


			for x in ipaddrlist:
				debug.Info ("    IP Address is "+str(x))

				if x.startswith("192.168."):
					debug.Info ("    At Home")
					atHome = True
				else:
					debug.Info ("    At Work")
					atHome = False

		except:
			debug.Exception ("Problem in detectHomeNetwork")
			
			
		debug.Info ("--- detectHomeNetwork ---")

		return atHome







	###############################################################################
	def send_email(self, message):
	###############################################################################
	#
	#
	###############################################################################

		debug=Debug()
		
		debug.Info ("+++ send_email +++")

		try:
			atHome=SocketControl.detectHomeNetwork(self)
			
			
			if atHome:
				me = "david.woods@btinternet.com"
				emailserver	="mail.btinternet.com"
			else:
				me = "david.woods@mformation.com" 
				emailserver	="mfemail04.mformation.com"


			you = "op_david_woods@yahoo.com"
			subject = "Home Control Status"

			debug.Info ("    To           ["+str(you)+"]")
			debug.Info ("    From         ["+str(me)+"]")
			debug.Info ("    Subject      ["+str(subject)+"]")
			debug.Info ("    Message      ["+str(message)+"]")
			debug.Info ("    Email Server ["+str(emailserver)+"]")

			# Create message container - the correct MIME type is multipart/alternative.
			msg = MIMEMultipart('alternative')
			msg['Subject'] = subject
			msg['From'] = me
			msg['To'] = you

			# Create the body of the message (a plain-text and an HTML version).
			text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
			html = "<html><head></head><body><font face=\"arial\"><p>Hi,<p>"+message+"</p></font></body></html>"

			# Record the MIME types of both parts - text/plain and text/html.
			part1 = MIMEText(text, 'plain')
			part2 = MIMEText(html, 'html')

			# Attach parts into message container.
			# According to RFC 2046, the last part of a multipart message, in this case
			# the HTML message, is best and preferred.
			msg.attach(part1)
			msg.attach(part2)

			# Send the message via local SMTP server.
			__hSocket = smtplib.SMTP(emailserver)

			# Auth Details if needed
			if atHome:
				__hSocket.login("david.woods", "Vulcan99")
			else:
				__hSocket.login("dwoods", "someboy1")

			__hSocket.sendmail(me, you, msg.as_string())
			__hSocket.quit()

		except:
			debug.Exception ("Problem in sending email")
			

		debug.Info ("--- send_email ---")
		
		
		
	###############################################################################
	def get_ip_address(self):
	###############################################################################
	# Get IP of Router - External
	#
	###############################################################################

		debug=Debug()
		debug.Info("+++ get_ip_address +++")

		addr=""
		titlestr = "What's My IP - Your IP is: "

		try:
			debug.Info("    Getting Page")
			response = urlopen("http://whatsmyip.net").read()

			x = response.index("<title>") + len("<title>")
			y = response.index("</title>")

			title = response[x:y]

			debug.Info("    Title is ["+str(title)+"]")

			if title.find(titlestr) > -1:
				addr = title.replace(titlestr, "")
				debug.Info("    IP Address found ["+str(addr)+"]")

		except Exception, e:
			debug.Exception("Problem in getting IP address. ["+str(e)+"]")


		debug.Info("--- get_ip_address ---")
		return addr
		
		






	
	
	
	

		
		



